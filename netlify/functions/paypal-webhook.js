const admin = require('firebase-admin');

// 1. تهيئة Firebase (باستخدام المفتاح الذي سنضعه في Netlify)
if (!admin.apps.length) {
  try {
    const serviceAccount = JSON.parse(process.env.FIREBASE_SERVICE_ACCOUNT_JSON);
    admin.initializeApp({
      credential: admin.credential.cert(serviceAccount),
      databaseURL: `https://${serviceAccount.project_id}.firebaseio.com`
    });
    console.log("✅ Firebase initialized successfully.");
  } catch (error) {
    console.error("❌ Firebase initialization failed:", error);
  }
}

// 2. دالة استقبال الدفع (Netlify Function)
exports.handler = async (event, context) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  try {
    // Netlify يرسل البيانات كنص (String)، لذا يجب تحويلها إلى JSON
    const body = JSON.parse(event.body);

    // التحقق من أن الحدث هو "تم الدفع بنجاح"
    if (body.event_type === 'PAYMENT.CAPTURE.COMPLETED') {
      const resource = body.resource;
      
      // استخراج معرف اللاعب من الرابط (custom_id)
      const playerId = resource.custom_id; 
      
      // حساب الشارات بناءً على المبلغ المدفوع
      const amount = parseFloat(resource.amount.value);
      let sparksToAdd = 500; // الافتراضي
      
      if (amount >= 20) sparksToAdd = 10000;
      else if (amount >= 8) sparksToAdd = 3800;
      else if (amount >= 4) sparksToAdd = 1600;

      if (playerId) {
        const db = admin.database();
        const userRef = db.ref(`players/${playerId}/sparks`);
        
        // إضافة الشارات (Atomic Transaction)
        await userRef.transaction((currentSparks) => {
          return (currentSparks || 0) + sparksToAdd;
        });

        console.log(`✅ Added ${sparksToAdd} sparks to player: ${playerId}`);
      }
    }

    return { statusCode: 200, body: JSON.stringify({ received: true }) };
  } catch (error) {
    console.error('❌ Webhook Error:', error);
    return { statusCode: 500, body: JSON.stringify({ error: 'Internal Server Error' }) };
  }
};

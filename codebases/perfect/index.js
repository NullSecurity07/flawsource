require('dotenv').config();

const config = {
    port: process.env.PORT || 3000,
    stripe: {
        secretKey: process.env.STRIPE_SECRET_KEY,
    },
    aws: {
        accessKey: process.env.AWS_ACCESS_KEY_ID,
    },
    isProduction: process.env.NODE_ENV === 'production'
};

// Fail fast if critical config is missing
if (!config.stripe.secretKey) {
    throw new Error("FATAL: STRIPE_SECRET_KEY is not defined.");
}

module.exports = config;
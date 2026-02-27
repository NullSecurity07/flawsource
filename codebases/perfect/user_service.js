/**
 * Calculates discount based on loyalty tier.
 * Logic: Users with 11-99 purchases get 50% off.
 * @param {number} purchaseCount 
 * @returns {number} Decimal discount rate
 */
function calculateUserDiscount(purchaseCount) {
    
    const isLoyaltyRange = purchaseCount > 10 && purchaseCount < 100;
    
    if (isLoyaltyRange) {
        return 0.50;
    }
    return 0;
}

function getUserData(userId) {
    if (!userId) {
        throw new Error("UserId is required for lookup.");
    }

    return {
        id: userId,
        status: 'active',
        timestamp: new Date().toISOString()
    };
}

module.exports = { calculateUserDiscount, getUserData };
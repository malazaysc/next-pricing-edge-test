import { InterfacePriceData } from "../types/Pricing.interface";
  
  export function calculatePrice(
    data: InterfacePriceData
  ): number {
    let totalPrice = 0;
    const { startDate, endDate, basePrice, rules } = data;

    const convertDate = (dateStr: string) => {
        const [year, month, day] = dateStr.split('-');
        return `${month}-${day}-${year}`;
      }

    // Calculate the total number of days
    let start = new Date(convertDate(startDate));
    const end = new Date(convertDate(endDate));
    const oneDay = 24 * 60 * 60 * 1000; // hours*minutes*seconds*milliseconds
    const totalDays = Math.round(Math.abs((start.getTime() - end.getTime()) / oneDay)) + 1;
  
    while(start <= end){
      let dayPrice = basePrice;
      const day = start.toISOString().split('T')[0]; // get YYYY-MM-DD format
  
      // Check if there's a rule for this day
      const applicableRules = rules.filter(rule => {
        if (rule.date && rule.date === day) return true;
        if (rule.minStayLength && totalDays >= rule.minStayLength) return true;
        return false;
      });
  
      if (applicableRules.length > 0) {
        // Sort the rules by priority (specific date > minimum stay length), 
        // and then by price modifier or fixed price
        applicableRules.sort((a, b) => {
          if (a.date && !b.date) return -1;
          if (!a.date && b.date) return 1;
          if (a.date && b.date) {
            if (a.fixedPrice !== undefined && b.fixedPrice !== undefined) {
              return b.fixedPrice - a.fixedPrice;
            } else if (a.priceModifier !== undefined && b.priceModifier !== undefined) {
              return b.priceModifier - a.priceModifier;
            }
          }
          if (a.minStayLength !== undefined && b.minStayLength !== undefined) {
            if (b.minStayLength - a.minStayLength !== 0) {
              return b.minStayLength - a.minStayLength;
            } else if (a.priceModifier !== undefined && b.priceModifier !== undefined) {
              return b.priceModifier - a.priceModifier;
            }
          }
          return 0;
        });
  
        const rule = applicableRules[0];
        if (rule.fixedPrice) {
          dayPrice = rule.fixedPrice;
        } else if (rule.priceModifier) {
          dayPrice = dayPrice + dayPrice * rule.priceModifier / 100;
        }
      }
  
      totalPrice += dayPrice;
      start = new Date(start.getTime() + oneDay);
    }
  
    return totalPrice;
  }
  
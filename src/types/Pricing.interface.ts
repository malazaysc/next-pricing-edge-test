export interface Rule {
    date?: string;
    minStayLength?: number;
    priceModifier?: number;  // priceModifier in percentage
    fixedPrice?: number;
  };

export interface InterfacePriceData {
    startDate: string,
    endDate: string,
    basePrice: number,
    rules: Rule[]
}
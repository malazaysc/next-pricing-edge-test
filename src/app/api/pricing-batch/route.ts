import { InterfacePriceData } from '@/components/types/Pricing.interface';
import { calculatePrice } from '../../../price/getPrice';

export const runtime = 'edge';

export const preferredRegion = 'auto';

interface ProductInterface extends InterfacePriceData {
    id: string
}

interface BodyInterface {
    products: ProductInterface[]
}

export async function POST(request: Request) {
    const body: BodyInterface = await request.json();
    const { products } = body;
    const response = products.map(product => {
        const totalPrice = calculatePrice(product);
        return {
            id: product.id,
            totalPrice,
        }
    });
    // const totalPrice = calculatePrice(body);
    return new Response(JSON.stringify(response), {
        headers: {
            'Content-Type': 'application/json',
        },
    });
}
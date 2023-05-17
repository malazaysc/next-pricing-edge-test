import { InterfacePriceData } from '@/components/types/Pricing.interface';
import { calculatePrice } from '../../../price/getPrice';

export const runtime = 'edge';

export const preferredRegion = 'auto';

interface BodyInterface extends InterfacePriceData {
    id: string
}

export async function POST(request: Request) {
    const body: BodyInterface = await request.json();
    console.log('body', body);
    const totalPrice = calculatePrice(body);
    return new Response(JSON.stringify({
        id: body.id,
        totalPrice,
    }), {
        headers: {
            'Content-Type': 'application/json',
        },
    });
}
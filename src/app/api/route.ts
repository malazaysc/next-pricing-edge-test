export async function GET(request: Request) {
    return new Response(JSON.stringify({
        message: 'Hello from pricing engine!',
    }), {
        headers: {
            'Content-Type': 'application/json',
        },
    });
}
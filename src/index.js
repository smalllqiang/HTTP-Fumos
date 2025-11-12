export default {
    async fetch(request, env) {
        const url = new URL(request.url);
        const code = url.pathname.replace("/", ""); // /404 -> 404
        try {
            const imageUrl = await env.fumo_status_images.get(code);
            if (!imageUrl) {
                return new Response("Not Found", { status: 404 });
            }
            const imageResponse = await fetch(imageUrl);
            if (!imageResponse.ok) {
                return new Response("Image Fetch Error", { status: 502 });
            }
            return new Response(await imageResponse.arrayBuffer(), {
        headers: { "Content-Type": "image/jpeg" },
            });
        } catch (err) {
            return new Response("Internal Error", { status: 500 });
        }
    },
};
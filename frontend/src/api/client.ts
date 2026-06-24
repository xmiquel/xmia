export async function fetchClient(path: string): Promise<unknown> {
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  const apiKey = import.meta.env.VITE_API_KEY;
  if (apiKey) {
    headers["X-API-Key"] = apiKey;
  }
  const res = await fetch(path, { headers });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail ?? "HTTP " + res.status);
  }
  return res.json();
}

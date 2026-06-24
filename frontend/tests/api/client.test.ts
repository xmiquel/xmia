import { describe, it, expect, vi, beforeEach } from "vitest";
import { fetchClient } from "../../src/api/client";

beforeEach(() => {
  vi.restoreAllMocks();
});

describe("fetchClient", () => {
  it("includes X-API-Key header when VITE_API_KEY is set", async () => {
    vi.stubEnv("VITE_API_KEY", "sk-test123");
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ status: "ok" }),
    });
    await fetchClient("/health");
    expect(fetch).toHaveBeenCalledWith("/health", {
      headers: expect.objectContaining({ "X-API-Key": "sk-test123" }),
    });
    vi.unstubAllEnvs();
  });

  it("omits X-API-Key header when VITE_API_KEY is not set", async () => {
    vi.stubEnv("VITE_API_KEY", "");
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ status: "ok" }),
    });
    await fetchClient("/health");
    const call = (fetch as ReturnType<typeof vi.fn>).mock.calls[0];
    expect(call[1].headers["X-API-Key"]).toBeUndefined();
    vi.unstubAllEnvs();
  });

  it("throws with detail on non-ok response", async () => {
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 401,
      json: () => Promise.resolve({ detail: "Invalid API Key" }),
    });
    await expect(fetchClient("/api/v1/account")).rejects.toThrow("Invalid API Key");
  });

  it("throws with HTTP status when no detail in body", async () => {
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 500,
      json: () => Promise.reject(new Error("no json")),
    });
    await expect(fetchClient("/error")).rejects.toThrow("HTTP 500");
  });
});

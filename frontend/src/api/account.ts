import { fetchClient } from "./client";
import type { AccountInfo } from "../types";

export function getAccountInfo(): Promise<AccountInfo> {
  return fetchClient("/api/v1/account") as Promise<AccountInfo>;
}

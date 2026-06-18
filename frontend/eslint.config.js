import js from "@eslint/js";
import reactPlugin from "eslint-plugin-react";
import reactHooks from "eslint-plugin-react-hooks";
import security from "eslint-plugin-security";
import globals from "globals";
import tseslint from "typescript-eslint";

export default [
  js.configs.recommended,
  ...tseslint.configs.strict,
  reactPlugin.configs.flat["jsx-runtime"],
  {
    plugins: {
      "react-hooks": reactHooks,
      security,
    },
    rules: {
      ...reactHooks.configs.recommended.rules,
      "security/detect-object-injection": "warn",
    },
    languageOptions: {
      globals: { ...globals.browser, ...globals.es2020 },
    },
    settings: {
      react: { version: "detect" },
    },
  },
];

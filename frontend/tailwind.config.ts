import type { Config } from "tailwindcss";
const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: { extend: {
    colors: { ink: "#14212b", mint: "#c8f7e4", aqua: "#23b5a6", coral: "#ff8b6a", cream: "#f8f7f2" },
    boxShadow: { soft: "0 18px 50px rgba(20,33,43,.08)" }
  }},
  plugins: []
};
export default config;

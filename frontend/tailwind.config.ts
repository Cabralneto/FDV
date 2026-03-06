import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        brand: "#0f172a",
        accent: "#0369a1"
      }
    }
  },
  plugins: []
};

export default config;

const withNextra = require("nextra")({
  theme: "nextra-theme-docs",
  themeConfig: "./theme.config.tsx",
});

/** @type {import("next").NextConfig} */
const config = {
  output: "export",
  images: {
    unoptimized: true,
  },
};

module.exports = withNextra(config);

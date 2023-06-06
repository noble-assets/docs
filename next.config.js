const withNextra = require("nextra")({
  theme: "nextra-theme-docs",
  themeConfig: "./theme.config.jsx",
});

/** @type {import("next").NextConfig} */
const config = {
  output: "export",
  basePath: "/docs",
  images: {
    unoptimized: true,
  },
};

module.exports = withNextra(config);

// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).
// There are various equivalent ways to declare your Docusaurus config.
// See: https://docusaurus.io/docs/api/docusaurus-config

import {themes as prismThemes} from 'prism-react-renderer';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Noble Docs',
  // tagline: 'Dinosaurs are cool',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://docs.noble.xyz/',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'noble-assets', // Usually your GitHub org/user name.
  projectName: 'docs', // Usually your repo name.

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          routeBasePath: '/', // Serve the docs at the site's root,

          sidebarPath: './sidebars.js',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/noble-assets/docs/tree/main/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/docusaurus-social-card.jpg',
      colorMode: {
        defaultMode: 'light',
        disableSwitch: false,
        respectPrefersColorScheme: false,
      },
      navbar: {
        title: 'Noble Docs',
        logo: {
          alt: 'My Site Logo',
          src: 'img/logo.svg',
        },
        items: [
          // {
          //   type: 'docSidebar',
          //   sidebarId: 'tutorialSidebar',
          //   position: 'left',
          //   label: 'Tutorial',
          // },
          {
            href: 'https://www.mintscan.io/noble/',
            position: 'left',
            label: 'Explorer'
          },
          {
            href: 'https://www.noble.xyz/#assets',
            position: 'left',
            label: 'Assets'
          },
          // {to: '/blog', label: 'Blog', position: 'left'},
          {
            label: 'Noble Express',
            href: 'https://express.noble.xyz/',
            position: 'right',
            className: 'launch-express',
          },
          {
            href: 'https://github.com/noble-assets/noble',
            className: 'pseudo-icon github-icon',
            position: 'right',
          },
          {
            href: 'https://noble.xyz',
            className: 'pseudo-icon web-icon',
            position: 'right',
          },

        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Other Docs',
            items: [
              // {
              //   label: 'Tutorial',
              //   to: '/docs/intro',
              // },
              {
                label: 'nobled Installation',
                href: 'https://github.com/noble-assets/noble#installation'
              },
              {
                label: 'Local Net Quick Start',
                href: 'https://github.com/noble-assets/noble/tree/main/local_net'
              }
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'X',
                href: 'https://x.com/noble_xyz',
              },
              {
                label: 'Discord',
                href: 'https://discord.gg/qefFy28Z',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'noble.xyz',
                href: 'https://noble.xyz',
              },
              {
                label: 'Brand Kit',
                href: 'https://drive.google.com/drive/folders/1Txc0MOsEz6wcSEu7h2CK24mMu4nIxEHw,'
              },
              {
                label: 'Contact',
                href: 'https://www.noble.xyz/#contact'
              }
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} NASD`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
    }),
};

export default config;

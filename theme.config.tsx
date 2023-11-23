import { useRouter } from "next/router";
import type { DocsThemeConfig } from "nextra-theme-docs";
import type { NextSeoProps } from "next-seo";

const config: DocsThemeConfig = {
  chat: {
    link: "https://twitter.com/noble_xyz",
    icon: (
      <svg width="24" height="24" viewBox="0 0 248 204">
        <path
          fill="currentColor"
          d="M221.95 51.29c.15 2.17.15 4.34.15 6.53 0 66.73-50.8 143.69-143.69 143.69v-.04c-27.44.04-54.31-7.82-77.41-22.64 3.99.48 8 .72 12.02.73 22.74.02 44.83-7.61 62.72-21.66-21.61-.41-40.56-14.5-47.18-35.07a50.338 50.338 0 0 0 22.8-.87C27.8 117.2 10.85 96.5 10.85 72.46v-.64a50.18 50.18 0 0 0 22.92 6.32C11.58 63.31 4.74 33.79 18.14 10.71a143.333 143.333 0 0 0 104.08 52.76 50.532 50.532 0 0 1 14.61-48.25c20.34-19.12 52.33-18.14 71.45 2.19 11.31-2.23 22.15-6.38 32.07-12.26a50.69 50.69 0 0 1-22.2 27.93c10.01-1.18 19.79-3.86 29-7.95a102.594 102.594 0 0 1-25.2 26.16z"
        />
      </svg>
    ),
  },
  docsRepositoryBase: "https://github.com/noble-assets/docs/tree/main",
  faviconGlyph: "✨",
  // @ts-ignore
  feedback: false,
  footer: {
    text: (
      <div>
        <p>© {new Date().getFullYear()} NASD Inc.</p>
      </div>
    ),
  },
  logo: (
    <>
      <svg
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M20.6524 0.00051244C19.7661 0.00281834 18.9167 0.356273 18.2904 0.98347C17.6641 1.61067 17.312 2.46048 17.311 3.34682V5.10652C16.3253 3.09895 14.6369 1.52298 12.5663 0.677537C10.4957 -0.167908 8.18677 -0.224024 6.07752 0.519831C4.30093 1.14968 2.7629 2.3141 1.67469 3.85316C0.586486 5.39223 0.00147215 7.23046 0 9.11536V20.6525C0 21.5402 0.352695 22.3917 0.980495 23.0195C1.6083 23.6472 2.45977 24 3.34762 24C4.23546 24 5.08695 23.6472 5.71474 23.0195C6.34255 22.3917 6.69525 21.5402 6.69525 20.6525V18.8965C7.68074 20.9033 9.36861 22.4785 11.4386 23.3233C13.5086 24.1681 15.8167 24.2237 17.925 23.4794C19.701 22.8498 21.2386 21.6856 22.3262 20.1471C23.4141 18.6084 23.9987 16.7707 24 14.8864V3.34682C23.9987 2.45952 23.6455 1.60894 23.018 0.981638C22.3904 0.354335 21.5396 0.00150065 20.6524 0.00051244ZM14.885 23.0735C13.1349 23.0808 11.429 22.5242 10.02 21.4864C8.61086 20.4486 7.57346 18.9846 7.06138 17.3111L7.04769 17.2625C6.81268 16.4924 6.6939 15.6916 6.69525 14.8864V9.11536C6.6959 8.47326 6.95135 7.85767 7.40552 7.40374C7.85967 6.94983 8.47542 6.69469 9.11753 6.69437C9.75901 6.69601 10.3737 6.95165 10.8272 7.40535C11.2807 7.85905 11.536 8.47389 11.5373 9.11536V14.884C11.5384 15.7717 11.8918 16.6228 12.5199 17.25C12.9886 17.7167 13.5848 18.0342 14.2336 18.1625C14.8823 18.2908 15.5546 18.2244 16.1655 17.9713C16.7766 17.7182 17.2989 17.2901 17.667 16.7406C18.0351 16.1912 18.2323 15.5452 18.2338 14.884V3.34682C18.2338 3.02906 18.2964 2.7144 18.4181 2.42082C18.5396 2.12724 18.7179 1.86048 18.9425 1.63579C19.1672 1.4111 19.434 1.23286 19.7276 1.11126C20.0213 0.989655 20.3358 0.927066 20.6536 0.927066C20.9715 0.927066 21.286 0.989655 21.5797 1.11126C21.8732 1.23286 22.1399 1.4111 22.3647 1.63579C22.5894 1.86048 22.7676 2.12724 22.8892 2.42082C23.0109 2.7144 23.0734 3.02906 23.0734 3.34682V14.884C23.0742 15.9594 22.8631 17.0247 22.4518 18.0186C22.0407 19.0125 21.4375 19.9156 20.6769 20.6762C19.9165 21.4368 19.0134 22.04 18.0196 22.4514C17.0258 22.8628 15.9606 23.0741 14.885 23.0735ZM17.311 14.884C17.3105 15.3624 17.1684 15.8301 16.9025 16.2278C16.6365 16.6258 16.2589 16.9359 15.817 17.1195C15.3751 17.303 14.8887 17.3516 14.4192 17.2591C13.9497 17.1667 13.5181 16.9373 13.1788 16.6C12.9302 16.3538 12.7385 16.0563 12.6171 15.7282C12.5947 15.6697 12.5748 15.6037 12.5548 15.5377L12.5474 15.5041L12.5399 15.4729C12.5287 15.4294 12.5175 15.3858 12.51 15.3397C12.51 15.3235 12.51 15.306 12.5013 15.2887V15.2624C12.5013 15.2214 12.4888 15.1804 12.4851 15.1379C12.4813 15.0956 12.4851 15.0869 12.4851 15.0533C12.4851 15.0196 12.4851 14.9699 12.4851 14.9287V9.11536C12.4843 8.67425 12.3965 8.23762 12.2267 7.83048C12.057 7.42334 11.8086 7.05366 11.4958 6.74262C11.183 6.43157 10.8119 6.18525 10.4039 6.01778C9.99577 5.85029 9.55866 5.76493 9.11753 5.76656C8.22966 5.76755 7.37844 6.1207 6.75062 6.7485C6.1228 7.37631 5.76966 8.22751 5.76866 9.11536V20.6525C5.76866 21.2945 5.5136 21.9103 5.05956 22.3643C4.60553 22.8183 3.98972 23.0735 3.34762 23.0735C2.70552 23.0735 2.08972 22.8183 1.63568 22.3643C1.18165 21.9103 0.926573 21.2945 0.926573 20.6525V9.11536C0.928013 7.15209 1.6346 5.25464 2.91765 3.7686C4.2007 2.28257 5.97484 1.30681 7.91695 1.01904C9.85906 0.731277 11.8399 1.15065 13.4988 2.20079C15.1576 3.25092 16.384 4.86195 16.9548 6.74045L16.9884 6.85004C17.2016 7.5863 17.3101 8.34888 17.311 9.11536V14.884Z"
          fill="url(#paint0_linear_3_13)"
        />
        <defs>
          <linearGradient
            id="paint0_linear_3_13"
            x1="1.64583"
            y1="22.3206"
            x2="30.246"
            y2="-6.32322"
            gradientUnits="userSpaceOnUse"
          >
            <stop offset="0.05" stopColor="currentColor" />
            <stop offset="0.38" stopColor="#A7B3FF" />
            <stop offset="1" stopColor="#74A4FF" />
          </linearGradient>
        </defs>
      </svg>

      <span style={{ marginLeft: ".5em", fontWeight: 750 }}>Noble</span>
    </>
  ),
  logoLink: "/",
  project: {
    link: "https://github.com/strangelove-ventures/noble",
  },
  sidebar: {
    defaultMenuCollapseLevel: 1,
  },
  head: (
    <>
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <meta name="description" content="Noble App Chain" />
      <meta name="og:title" content="Noble" />
    </>
  ),
  useNextSeoProps(): NextSeoProps {
    const { route } = useRouter();

    if (route !== "/") {
      return {
        titleTemplate: "%s – Noble",
      };
    }
  },
};

export default config;

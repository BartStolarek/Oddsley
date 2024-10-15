# Frontend Next.js App

## Technologies Used

- [Next.js 14](https://nextjs.org/docs/getting-started)
- [NextUI v2](https://nextui.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Tailwind Variants](https://tailwind-variants.org)
- [TypeScript](https://www.typescriptlang.org/)
- [Framer Motion](https://www.framer.com/motion/)
- [next-themes](https://github.com/pacocoursey/next-themes)

## Theme Colours

### Using Colours

1. Import semantic and common colours into your component as follows:
```
import {commonColors, semanticColors} from "@nextui-org/theme";
```

2. Use the colours in your component as follows:
```
/* With default prefix */
.my-component {
  background-color: hsl(var(--nextui-primary-500));
}
/*  With custom prefix */
.my-component {
  background-color: hsl(var(--myapp-primary-500));
}
```

### Changing Colours

1. Open `tailwind.config.js`

2. Change the colors in the following details:
```
module.exports = {
  plugins: [
    nextui({
      themes: {
        light: {
          colors: {
            // Layout
            background: "#FFFFFF",
            foreground: "#11181C",
            divider: "rgba(0, 0, 0, 0.15)",
            focus: "#006FEE",

            // Content
            content1: "#FFFFFF",
            content2: "#F4F4F5",
            content3: "#E4E4E7",
            content4: "#D4D4D8",

            // Base
            default: "#71717A",
            primary: {
              50: '#001731',
              100: '#002e62',
              200: '#004493',
              300: '#005bc4',
              400: '#006FEE',
              500: '#338ef7',
              600: '#66aaf9',
              700: '#99c7fb',
              800: '#cce3fd',
              900: '#e6f1fe',
              foreground: "#FFFFFF",
              DEFAULT: "#006FEE",
            },
            secondary: {
              50: '#180828',
              100: '#301050',
              200: '#481878',
              300: '#6020a0',
              400: '#7828c8',
              500: '#9353d3',
              600: '#ae7ede',
              700: '#c9a9e9',
              800: '#e4d4f4',
              900: '#f2eafa',
              foreground: "#FFFFFF",
              DEFAULT: "#9353d3",
            },
            success: {
              50: '#052814',
              100: '#095028',
              200: '#0e793c',
              300: '#12a150',
              400: '#17c964',
              500: '#45d483',
              600: '#74dfa2',
              700: '#a2e9c1',
              800: '#d1f4e0',
              900: '#e8faf0',
              foreground: "#FFFFFF",
              DEFAULT: "#17c964",
            },
            warning: {
              50: '#312107',
              100: '#62420e',
              200: '#936316',
              300: '#c4841d',
              400: '#f5a524',
              500: '#f7b750',
              600: '#f9c97c',
              700: '#fbdba7',
              800: '#fdedd3',
              900: '#fefce8',
              foreground: "#FFFFFF",
              DEFAULT: "#f5a524",
            },
            danger: {
              50: '#310413',
              100: '#610726',
              200: '#920b3a',
              300: '#c20e4d',
              400: '#f31260',
              500: '#f54180',
              600: '#f871a0',
              700: '#faa0bf',
              800: '#fdd0df',
              900: '#fee7ef',
              foreground: "#FFFFFF",
              DEFAULT: "#f31260",
            },

            // Default
            default: {
              50: '#fafafa',
              100: '#f4f4f5',
              200: '#e4e4e7',
              300: '#d4d4d8',
              400: '#a1a1aa',
              500: '#71717a',
              600: '#52525b',
              700: '#3f3f46',
              800: '#27272a',
              900: '#18181b',
              foreground: "#FFFFFF",
              DEFAULT: "#71717A",
            },
          },
        },
        dark: {
          colors: {
            // Layout
            background: "#000000",
            foreground: "#ECEDEE",
            divider: "rgba(255, 255, 255, 0.15)",
            focus: "#006FEE",

            // Content
            content1: "#18181b",
            content2: "#27272a",
            content3: "#3f3f46",
            content4: "#52525b",

            // Base colors remain the same as in light theme
            // Default, Primary, Secondary, Success, Warning, Danger
            // are the same as in the light theme
          },
        },
      },
    }),
  ],
}

```

Note:
For more information visit [NextUI Colors](https://nextui.org/docs/customization/colors#javascript-variables)


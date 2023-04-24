/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    publicRuntimeConfig: {
        FLASK_APP_URL: process.env.FLASK_APP_URL,
    },
};

module.exports = nextConfig;

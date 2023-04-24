import { createTheme, ThemeProvider } from '@mui/material/styles';
import 'react-toastify/dist/ReactToastify.css';
import { ToastContainer } from 'react-toastify';
import '@/styles/globals.css';
import Navbar from '@/components/navbar';
import Footer from '@/components/footer';

const theme = createTheme({
    palette: {
        mode: 'light',
        primary: {
            main: '#24292e',
        },
        secondary: {
            main: '#6a737d',
        },
    },
});

export default function MyApp({ Component, pageProps }) {
    return (
        <ThemeProvider theme={theme}>
            <Navbar />
            <Component {...pageProps} />
            <ToastContainer />
            <Footer />
        </ThemeProvider>
    );
}

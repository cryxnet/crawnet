import { useState } from 'react';
import { Box, Button, TextField, useTheme, Typography, Link, Backdrop, CircularProgress } from '@mui/material';
import { toast } from 'react-toastify';
import { useRouter } from 'next/router';
import getConfig from 'next/config';

export default function DomainDiscover() {
    const [domain, setDomain] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const router = useRouter();

    const { publicRuntimeConfig } = getConfig();
    const apiUrl = publicRuntimeConfig.FLASK_APP_URL;

    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();

        setIsLoading(true);

        toast('🫡 Request sent to intelligence service', {
            position: 'top-center',
            hideProgressBar: true,
            autoClose: 2000,
            type: 'info',
        });
        try {
            const response = await fetch(`${apiUrl}/domain/${domain}`, {
                method: 'POST',
            });

            toast('✨ Successfully gathered information about the domain... redirecting...', {
                position: 'top-center',
                hideProgressBar: true,
                autoClose: 2000,
                type: 'success',
            });

            router.push('/graph');
        } catch (error) {
            toast('😞 An error occured during the data collection, please check the logs.', {
                position: 'top-center',
                hideProgressBar: true,
                autoClose: 2000,
                type: 'error',
            });

            console.log(error);
        }
    };

    return (
        <Box
            display="flex"
            flexDirection="column"
            alignItems="center"
            justifyContent="center"
            height="100vh"
            maxWidth="600px"
            margin="0 auto"
            padding="0 16px"
            textAlign="center"
            className="search_container"
            sx={{ mt: '-10vh' }}
        >
            {isLoading && (
                <Backdrop open={true} sx={{ zIndex: 999 }}>
                    <CircularProgress color="secondary" size={100} />
                </Backdrop>
            )}
            <Typography variant="h4" component="h1" gutterBottom>
                Discover domains with CRAWNET
            </Typography>

            <Box marginBottom="16px" width="100%">
                <TextField
                    id="outlined-search"
                    label="Enter a domain name"
                    type="search"
                    fullWidth
                    value={domain}
                    onChange={(event) => setDomain(event.target.value)}
                />
            </Box>
            <Button variant="contained" sx={{ bgcolor: 'black' }} onClick={handleSubmit}>
                Execute
            </Button>
            <Box marginTop="32px">
                <Typography variant="body2" gutterBottom>
                    Powered by CRYXNET -{' '}
                    <Link href="https://github.com/cryxnet/crawnet" target="_blank">
                        Github repository
                    </Link>{' '}
                    -{' '}
                    <Link href="https://www.cryxnet.com" target="_blank">
                        www.cryxnet.com
                    </Link>
                </Typography>
            </Box>
        </Box>
    );
}

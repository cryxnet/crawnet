import { Box, Button, Container, Link, Typography } from '@mui/material';
import { createTheme, ThemeProvider } from '@mui/material/styles';

const theme = createTheme({
    palette: {
        primary: {
            main: '#000',
        },
        secondary: {
            main: '#000',
        },
        background: {
            default: '#F4F4F4',
        },
    },
});

export default function LandingPage() {
    return (
        <ThemeProvider theme={theme}>
            <Box
                sx={{
                    width: '100vw',
                    minHeight: '100vh',
                    overflow: 'hidden',
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'space-between',
                    alignItems: 'center', // center horizontally
                }}
            >
                <Container maxWidth="sm" sx={{ flexGrow: 1, marginTop: 20 }}>
                    <Box sx={{ my: 4 }}>
                        <Typography variant="h4" component="h1" gutterBottom>
                            Welcome to CRAWNET
                        </Typography>
                        <Typography variant="body1" gutterBottom>
                            CRAWNET is a graph-based domain discovery tool by CRYXNET that helps you gather information
                            about domains and potential relationships with other actors.
                        </Typography>
                        <Typography variant="body1" gutterBottom>
                            With the power of graph databases, each node in the graph represents a domain and its
                            attributes, such as DNS records, IP addresses, and services related to the IP. With that we
                            can easily discover any relationships between the actors.
                        </Typography>
                        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', mt: 4 }}>
                            <Box sx={{ mr: 2 }}>
                                <Button
                                    variant="contained"
                                    sx={{ bgcolor: 'secondary.main' }}
                                    component={Link}
                                    href="/discover"
                                >
                                    Discover
                                </Button>
                            </Box>
                            <Box sx={{ ml: 2 }}>
                                <Button
                                    variant="contained"
                                    sx={{ bgcolor: 'secondary.main' }}
                                    component={Link}
                                    href="/graph"
                                >
                                    Graph
                                </Button>
                            </Box>
                        </Box>
                    </Box>
                </Container>
            </Box>
        </ThemeProvider>
    );
}

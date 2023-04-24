import { Box, Link, Typography } from '@mui/material';

export default function Navbar() {
    return (
        <Box sx={{ bgcolor: 'primary.main', color: 'white', py: 2, position: 'absolute', bottom: 0, width: '100%' }}>
            <Typography variant="body2" align="center">
                &copy; {new Date().getFullYear()} CRYXNET |{' '}
                <Link href="https://github.com/cryxnet/crawnet" color="inherit" underline="always">
                    GitHub Repository
                </Link>{' '}
                |{' '}
                <Link href="https://cryxnet.com" color="inherit" underline="always">
                    cryxnet.com
                </Link>
            </Typography>
        </Box>
    );
}

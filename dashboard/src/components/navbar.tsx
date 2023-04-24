import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Link from '@mui/material/Link';

export default function Navbar() {
    return (
        <AppBar position="static" sx={{ bgcolor: 'black', width: '100vw', margin: '0 auto' }}>
            <Toolbar sx={{ width: '80vw', margin: '0 auto' }}>
                <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontWeight: 'bold' }}>
                    CRAWNET
                </Typography>
                <Button color="inherit" component={Link} href="/">
                    Home
                </Button>
                <Button color="inherit" component={Link} href="/discover">
                    Discover
                </Button>
                <Button color="inherit" component={Link} href="/graph">
                    Graph
                </Button>
            </Toolbar>
        </AppBar>
    );
}

import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#90caf9',
    },
    secondary: {
      main: '#f48fb1',
    },
    background: {
      default: '#121212',
      paper: '#1d1d1d',
    },
    text: {
      primary: '#ffffff',
      secondary: '#aaaaaa',
    },
  },
  typography: {
    h3: {
      fontFamily: 'Roboto, sans-serif',
      fontWeight: 300,
      letterSpacing: '0.0075em',
    },
    body1: {
      fontFamily: 'Roboto, sans-serif',
      fontWeight: 300,
      letterSpacing: '0.0075em',
    },
  },
});

export default theme;

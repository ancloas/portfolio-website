import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#90caf9', // Default color
    },
    secondary: {
      main: '#f48fb1', // Default color
    },
    background: {
      default: '#2a2b33', // Default color
      paper: '#434945', // Default color
    },
    text: {
      primary: '#ffffff', // Default color
      secondary: '#aaaaaa', // Default color
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

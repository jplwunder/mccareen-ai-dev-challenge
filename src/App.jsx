import { useState, useMemo, useEffect } from "react";

import {
  Box,
  Container,
  Stack,
  TextField,
  Button,
  Grid,
  Typography,
} from "@mui/material";
import ManageSearchRoundedIcon from "@mui/icons-material/ManageSearchRounded";

function App() {
  // states
  const [width, setWidth] = useState(window.innerWidth);
  const [websiteUrl, setWebsiteUrl] = useState("");

  // variables
  const isMobile = useMemo(() => width <= 768, [width]);

  // functions
  function handleWindowSizeChange() {
    setWidth(window.innerWidth);
  }

  // effects
  useEffect(() => {
    window.addEventListener("resize", handleWindowSizeChange);
    return () => {
      window.removeEventListener("resize", handleWindowSizeChange);
    };
  }, []);

  return (
    <Container maxWidth={isMobile ? "xs" : "md"}>
      <Stack
        spacing={4}
        direction={isMobile ? "column" : "row"}
        justifyContent="center"
        alignItems="center"
        sx={{ height: "95vh" }}
      >
        <Stack spacing={2} sx={{ width: "100%" }}>
          <Typography noWrap={isMobile ? false : true} variant="h4">
            Company Profile Generator
          </Typography>
          <Typography variant="body1">
            Analyze any company website to generate comprehensive business
            profiles.
          </Typography>
        </Stack>

        <Stack direction="row" spacing={1} sx={{ width: "100%" }}>
          <TextField
            fullWidth
            variant="outlined"
            placeholder="https://website.com"
            value={websiteUrl}
            onChange={(e) => setWebsiteUrl(e.target.value)}
          />
          <Button
            onClick={() => console.log("Generate profile for:", websiteUrl)}
            disabled={!websiteUrl.trim()}
            variant="contained"
            color="primary"
          >
            <ManageSearchRoundedIcon />
          </Button>
        </Stack>
      </Stack>
    </Container>
  );
}

export default App;

import { useState, useMemo, useEffect } from "react";

import {
  Container,
  Stack,
  TextField,
  Button,
  Typography,
  Card,
  CardHeader,
  CardContent,
  CardActions,
} from "@mui/material";
import ManageSearchRoundedIcon from "@mui/icons-material/ManageSearchRounded";

import CompanyReportCard from "./CompanyReportCard";

function App() {
  // states
  const [width, setWidth] = useState(window.innerWidth);
  const [isLoading, setIsLoading] = useState(false);
  const [companyProfileData, setCompanyProfileData] = useState(null);
  const [error, setError] = useState(null);

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

  const handleGenerateProfile = async () => {
    const url = `http://localhost:8000/api/analyze-website?website_url=${encodeURIComponent(
      websiteUrl.trim()
    )}`;
    if (!/^https?:\/\/[\w.-]+\.[a-z]{2,}/i.test(websiteUrl.trim())) {
      setError(
        "Please enter a valid website URL (including http:// or https://)."
      );
      return;
    }
    try {
      setIsLoading(true);
      const response = await fetch(url, {
        method: "POST",
      });
      const data = await response.json();
      if (!response.ok) {
        setError("Failed to generate profile. Please try again.");
        throw new Error(data.detail || "Failed to generate profile");
      }
      setCompanyProfileData({ ...companyProfileData, ...data });
    } catch (error) {
      console.error("Error generating profile:", error);
      setError("Failed to generate profile. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  console.log("Company Profile Data:", companyProfileData);

  return (
    <Container maxWidth={isMobile ? "xs" : "md"} sx={{ mt: 4 }}>
      <Stack spacing={2} sx={{ mb: 4 }} alignItems={"center"}>
        <Stack
          spacing={4}
          direction={isMobile ? "column" : "row"}
          justifyContent="center"
          alignItems="center"
          sx={{
            height: isLoading || companyProfileData ? "auto" : "90vh",
          }}
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

          <Stack
            direction="row"
            spacing={1}
            alignItems={"flex-start"}
            sx={{ width: "100%" }}
          >
            <TextField
              fullWidth
              variant="outlined"
              placeholder="https://website.com"
              value={websiteUrl}
              helperText={error}
              onChange={(e) => {
                setError(null);
                setWebsiteUrl(e.target.value);
              }}
            />
            <Button
              onClick={handleGenerateProfile}
              disabled={!websiteUrl.trim()}
              variant="text"
              color="primary"
              sx={{
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                height: "56px",
                minWidth: "56px",
                p: 0,
              }}
            >
              <ManageSearchRoundedIcon sx={{ fontSize: 48 }} />
            </Button>
          </Stack>
        </Stack>

        {isLoading && (
          <Card sx={{ width: isMobile ? "100%" : "80%", marginTop: 2 }}>
            <Stack spacing={2} sx={{ padding: 2 }}>
              <CardHeader title="Loading..." />
              <CardContent>
                <Typography variant="body1">
                  Please wait... Profile generations can take up to a couple of
                  minutes.
                </Typography>
              </CardContent>
              <CardActions>
                <Stack
                  direction="row"
                  spacing={1}
                  justifyContent="flex-end"
                  flexGrow={1}
                ></Stack>
              </CardActions>
            </Stack>
          </Card>
        )}

        {companyProfileData && !isLoading && (
          <CompanyReportCard
            isMobile={isMobile}
            isLoading={isLoading}
            initialCompanyProfileData={companyProfileData}
          />
        )}
      </Stack>
    </Container>
  );
}

export default App;

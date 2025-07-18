import PropTypes from "prop-types";
import { useState } from "react";

import {
  Box,
  Card,
  CardContent,
  CardHeader,
  CardActions,
  Stack,
  TextField,
  Button,
  Typography,
  Divider,
} from "@mui/material";

CompanyReportCard.propTypes = {
  isLoading: PropTypes.bool.isRequired,
  initialCompanyProfileData: PropTypes.shape({
    company_name: PropTypes.string,
    service_lines: PropTypes.arrayOf(PropTypes.string),
    company_description: PropTypes.string,
    tier1_keywords: PropTypes.arrayOf(PropTypes.string),
    tier2_keywords: PropTypes.arrayOf(PropTypes.string),
    emails: PropTypes.arrayOf(PropTypes.string),
    point_of_contact: PropTypes.arrayOf(PropTypes.string),
  }).isRequired,
};

function CompanyReportCard({ isLoading, initialCompanyProfileData }) {
  const [mode, setMode] = useState("view");

  const [companyProfileData, setCompanyProfileData] = useState({
    ...initialCompanyProfileData,
    service_lines: initialCompanyProfileData?.service_lines.map((line) =>
      line.trim()
    ) || ["Unknown"],
    tier1_keywords: initialCompanyProfileData?.tier1_keywords.map((keyword) =>
      keyword.trim()
    ) || ["Unknown"],
    tier2_keywords: initialCompanyProfileData?.tier2_keywords.map((keyword) =>
      keyword.trim()
    ) || ["Unknown"],
    emails: initialCompanyProfileData?.emails.map((email) => email.trim()) || [
      "Unknown",
    ],
  });

  if (mode === "edit") {
    return (
      <>
        <Card
          sx={{
            width: "100%",
            marginTop: 2,
          }}
        >
          <Stack spacing={2} sx={{ padding: 2 }}>
            <TextField
              disabled={isLoading}
              fullWidth
              label="Company Name"
              value={companyProfileData?.company_name || ""}
              variant="outlined"
              onChange={(e) =>
                setCompanyProfileData({
                  ...companyProfileData,
                  company_name: e.target.value,
                })
              }
            />
            <TextField
              disabled={isLoading}
              fullWidth
              label="Company Description"
              value={companyProfileData?.company_description || ""}
              multiline
              rows={4}
              variant="outlined"
              onChange={(e) =>
                setCompanyProfileData({
                  ...companyProfileData,
                  company_description: e.target.value,
                })
              }
            />
            <Stack spacing={0.5}>
              <Typography variant="subtitle1">Service lines:</Typography>
              <TextField
                disabled={isLoading}
                fullWidth
                helperText="Comma-separated list"
                value={companyProfileData?.service_lines?.join(", ") || ""}
                variant="outlined"
                margin="normal"
                onChange={(e) =>
                  setCompanyProfileData({
                    ...companyProfileData,
                    service_lines: e.target.value.split(", "),
                  })
                }
              />
            </Stack>

            <Stack spacing={0.5}>
              <Typography variant="subtitle1">Tier 1 Keywords:</Typography>
              <TextField
                disabled={isLoading}
                fullWidth
                helperText="Comma-separated list"
                value={companyProfileData?.tier1_keywords?.join(", ") || ""}
                variant="outlined"
                margin="normal"
                onChange={(e) =>
                  setCompanyProfileData({
                    ...companyProfileData,
                    tier1_keywords: e.target.value.split(", "),
                  })
                }
              />
            </Stack>

            <Stack spacing={0.5}>
              <Typography variant="subtitle1">Tier 2 Keywords:</Typography>
              <TextField
                disabled={isLoading}
                fullWidth
                helperText="Comma-separated list"
                value={companyProfileData?.tier2_keywords?.join(", ") || ""}
                variant="outlined"
                margin="normal"
                onChange={(e) =>
                  setCompanyProfileData({
                    ...companyProfileData,
                    tier2_keywords: e.target.value.split(", "),
                  })
                }
              />
            </Stack>

            <Stack spacing={0.5}>
              <Typography variant="subtitle1">Emails:</Typography>
              <TextField
                disabled={isLoading}
                fullWidth
                helperText="Comma-separated list"
                value={companyProfileData?.emails?.join(", ") || ""}
                variant="outlined"
                margin="normal"
                onChange={(e) =>
                  setCompanyProfileData({
                    ...companyProfileData,
                    emails: e.target.value.split(", "),
                  })
                }
              />
            </Stack>

            <Stack spacing={0.5}>
              <Typography variant="subtitle1">Points of Contact:</Typography>
              <TextField
                disabled={isLoading}
                fullWidth
                helperText="Comma-separated list"
                value={companyProfileData?.point_of_contact?.join(", ") || ""}
                variant="outlined"
                margin="normal"
                onChange={(e) =>
                  setCompanyProfileData({
                    ...companyProfileData,
                    point_of_contact: e.target.value.split(", "),
                  })
                }
              />
            </Stack>
            <CardActions>
              <Stack
                direction="row"
                spacing={1}
                justifyContent="flex-end"
                flexGrow={1}
              >
                <Button size="small" onClick={() => setMode("view")}>
                  Save
                </Button>
              </Stack>
            </CardActions>
          </Stack>
        </Card>
      </>
    );
  } else if (mode === "view") {
    return (
      <Card sx={{ width: "100%", marginTop: 2 }}>
      <Stack spacing={2} sx={{ padding: 2 }}>
        <CardHeader
        title={
          <Typography variant="h3">
          {companyProfileData?.company_name || "Unknown company name"}
          </Typography>
        }
        />
        <Divider />
        <CardContent>
        <Typography variant="body1" gutterBottom>
          {companyProfileData?.company_description ||
          "Unknown company description"}
        </Typography>
        <Box mt={2}>
          <Typography variant="subtitle1" fontWeight="bold">
          Service lines:
          </Typography>
          {companyProfileData?.service_lines &&
          companyProfileData.service_lines.length > 0 ? (
          companyProfileData.service_lines.map((line, idx) => (
            <Typography key={idx} variant="body2">
            {line}
            </Typography>
          ))
          ) : (
          <Typography variant="body2">Unknown</Typography>
          )}
        </Box>
        <Box mt={2}>
          <Typography variant="subtitle1" fontWeight="bold">
          Tier 1 Keywords:
          </Typography>
          {companyProfileData?.tier1_keywords &&
          companyProfileData.tier1_keywords.length > 0 ? (
          companyProfileData.tier1_keywords.map((keyword, idx) => (
            <Typography key={idx} variant="body2">
            {keyword}
            </Typography>
          ))
          ) : (
          <Typography variant="body2">Unknown</Typography>
          )}
        </Box>
        <Box mt={2}>
          <Typography variant="subtitle1" fontWeight="bold">
          Tier 2 Keywords:
          </Typography>
          {companyProfileData?.tier2_keywords &&
          companyProfileData.tier2_keywords.length > 0 ? (
          companyProfileData.tier2_keywords.map((keyword, idx) => (
            <Typography key={idx} variant="body2">
            {keyword}
            </Typography>
          ))
          ) : (
          <Typography variant="body2">Unknown</Typography>
          )}
        </Box>
        <Box mt={2}>
          <Typography variant="subtitle1" fontWeight="bold">
          Emails:
          </Typography>
          {companyProfileData?.emails &&
          companyProfileData.emails.length > 0 ? (
          companyProfileData.emails.map((email, idx) => (
            <Typography key={idx} variant="body2">
            {email}
            </Typography>
          ))
          ) : (
          <Typography variant="body2">Unknown</Typography>
          )}
        </Box>
        <Box mt={2}>
          <Typography variant="subtitle1" fontWeight="bold">
          Points of Contact:
          </Typography>
          {companyProfileData?.point_of_contact &&
          companyProfileData.point_of_contact.length > 0 ? (
          companyProfileData.point_of_contact.map((contact, idx) => (
            <Typography key={idx} variant="body2">
            {contact}
            </Typography>
          ))
          ) : (
          <Typography variant="body2">Unknown</Typography>
          )}
        </Box>
        </CardContent>
        <CardActions>
        <Stack
          direction="row"
          spacing={1}
          justifyContent="flex-end"
          flexGrow={1}
        >
          <Button size="small" onClick={() => setMode("edit")}>
          Edit
          </Button>
          <Button
          size="small"
          onClick={() => {
            const json = JSON.stringify(companyProfileData, null, 2);
            const blob = new Blob([json], { type: "application/json" });
            const url = URL.createObjectURL(blob);
            window.open(url, "_blank");
            setTimeout(() => URL.revokeObjectURL(url), 1000);
          }}
          >
          View JSON
          </Button>
        </Stack>
        </CardActions>
      </Stack>
      </Card>
    );
  }
}

export default CompanyReportCard;

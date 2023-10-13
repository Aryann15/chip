import React, { useEffect } from "react";
import Box from "@mui/material/Box";
import Card from "@mui/material/Card";
import TextField from "@mui/material/TextField";
import { Typography } from "@mui/material";
import Button from "@mui/material/Button";
import { useState } from "react";

const Review = () => {
  const [product, setProduct] = useState(null);

  const handleProduct = (event) => {
    setProduct(event.target.value);
  };


    const handleSubmit = async () => {
      const formData = new FormData();
      formData.append("product", product);

      try {
        const response = await fetch("http://localhost:5000/review", {
          method: "POST",
          body: formData,
        });

        if (response.ok) {
          const result = await response.text();
          alert(result);
        } else {
          alert("Something is wrong");
        }
      } catch (error) {
        console.error("Error", error);
      }
    };
  }

  return (
    <>
      <Box sx={{ bgcolor: "#737CA1", height: "100vh" }}>
        <br />
        <Typography
          variant="h5"
          align="center"
          gutterBottom
          sx={{ mb: 2 }}
          color="#FFFFFF"
        >
          Get a Detailed Review about your product!
        </Typography>
        <Card
          variant="outlined"
          sx={{
            maxWidth: 400,
            maxHeight: 300,
            p: 3,
            mx: "auto",
            bgcolor: "#95B9C7",
          }}
        >
          <Typography
            variant="h6"
            align="center"
            gutterBottom
            sx={{ mb: 1.5 }}
            color="#00000"
          >
            Your Product name
          </Typography>
          <TextField
            id="outlined-basic"
            label="Product name"
            variant="outlined"
            onChange={handleProduct}
            style={{ width: 400, backgroundColor: "#E3E4FA" }}
          />
          <br />
          <br />
          <div style={{ display: "flex", justifyContent: "center" }}>
            <Button
              variant="contained"
              onClick={handleSubmit}
              style={{ width: 100, backgroundColor: "#4169E1" }}
            >
              submit
            </Button>
            {console.log(product)}
          </div>
        </Card>
      </Box>
    </>
  );
};

export default Review;

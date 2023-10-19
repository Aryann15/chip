import React from "react";
import { useState } from "react";
import Card from "@mui/material/Card";
import TextField from "@mui/material/TextField";
import { Typography } from "@mui/material";
import Button from "@mui/material/Button";
import "./Home.css";
const Home = () => {
  const [buttons, setButtons] = useState(false);
  const [product, setProduct] = useState();

  const handleProduct = (event) => {
    setProduct(event.target.value);
  };

  const handleSubmit = async () => {
    try {
      const formData = new FormData();
      formData.append("product", product);
      const response = await fetch("http://localhost:5000/", {
        method: "POST",
        body: formData,
      });
      console.log(response.ok);
      console.log(response.status);

      if (response.ok) {
        const data = await response.json();
        setButtons(true);
        console.log(data);
      } else {
        throw new Error("Something went wrong");
      }
    } catch (error) {
      alert(error.message);
    }
  };

  return (
    <div className="home">
      <Typography variant="h6" gutterBottom sx={{ mb: 1.5 }} color="#00000">
        Your Product name
      </Typography>

      <TextField
        id="outlined-basic"
        label="Product"
        variant="outlined"
        onChange={handleProduct}
        style={{ width: 400, backgroundColor: "#E3E4FA" }}
      />
      <br />
      <br />
      <div className="button-container">
        
        <div style={{ display: "flex", justifyContent: "center", flexDirection:"column" }}>
          <Button
            variant="contained"
            onClick={handleSubmit}
            style={{ width: 100, height: 50, backgroundColor: "#4169E1" }}
          >
            submit
          </Button>
          <br />

          {buttons ? (
            <div>
              <Button
                variant="contained"
                onClick={handleSubmit}
                style={{ width: 100, backgroundColor: "#2E4053" }}
              >
             
                Review
              </Button>

              <Button
                variant="contained"
                onClick={handleSubmit}
                style={{ width: 100, backgroundColor: "#2E4053" }}
              >
                
                QnA
              </Button>
            </div>
          ) : null}

          {/* {console.log(product)} */}
        </div>
      </div>
    </div>
  );
};

export default Home;

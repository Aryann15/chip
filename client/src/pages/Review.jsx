import React from "react";
import Box from "@mui/material/Box";
import Card from "@mui/material/Card";
import TextField from "@mui/material/TextField";
import { Typography } from "@mui/material";
import Button from "@mui/material/Button";
import { useState } from "react";
import { useEffect } from "react";
import "./styles.css";
import UserMessage from "../components/UserMessage";
import BotMessage from "../components/BotMessage";

const Review = () => {
  const [query, setQuery] = useState(null);
  const [messages, setMessages] = useState([]);
  const [questions, setQuestions] = useState();
  const [chatHistory, setChatHistory] = useState([]); 

  const handleQuery = (event) => {
    setQuery(event.target.value);
  };

  const handleSubmit = async () => {
    try {
      // const json = JSON.stringify({ query });
      const formData = new FormData();
      formData.append("query", query);
      // JSON.parse(json);
      const response = await fetch("http://localhost:5000/review", {
        method: "POST",
        body: formData,
      });
      console.log(response.ok);
      console.log(response.status);

      if (response.ok) {
        const data = await response.json();
        setChatHistory([...chatHistory, { type: 'user', content: data.question }]);
        setChatHistory([...chatHistory, { type: 'bot', content: data.answer }]);
       
        setMessages(data.answer);
        console.log(data);
        setQuestions(data.question);
      } else {
        throw new Error("Something went wrong");
      }
    } catch (error) {
      alert(error.message);
    }
  };

  const responses = [
    { type: "user", content: questions },
    { type: "bot", content: messages },
  ];

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
            onChange={handleQuery}
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
            {/* {console.log(product)} */}
          </div>
        </Card>
        <Typography
          variant="h7"
          align="center"
          gutterBottom
          sx={{ mb: 2 }}
          color="#FFFFFF"
        >
           {chatHistory.map((message, index) => {
            if (message.type === 'user') {
              return <UserMessage key={index} message={message.content} />;
            } else if (message.type === 'bot') {
              return <BotMessage key={index} message={message.content} />;
            } else {
              return null;
            }
          })}

        </Typography>
      </Box>
    </>
  );
};

export default Review;

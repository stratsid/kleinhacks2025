import React, {use, useEffect, useState} from "react";

function index() {

  const [message, setMessage] = useState("Loading...");

  useEffect(() => {
    fetch("http://localhost:8000/hello")
      .then((response) => response.json())
      .then((data) => {setMessage(data.message)});
  }, []);

  return <div>{message}</div>
}

export default index;
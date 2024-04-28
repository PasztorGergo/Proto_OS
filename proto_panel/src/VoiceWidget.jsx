import React, { useEffect } from "react";
import { useRhino } from "@picovoice/rhino-react";
import { modelParams } from "../model";

function VoiceWidget(props) {
  const {
    inference,
    contextInfo,
    isLoaded,
    isListening,
    error,
    init,
    process,
    release,
  } = useRhino();

  const rhinoContext = {
    base64:
      "cmhpbm8zLjAuMGVuABMAAABHaXRIdWJPSURDXzgwOTY5NjQ0//////////8AAAAAbAQAAAQAAABjb250ZXh0OgogIGV4cHJlc3Npb25zOgogICAgdm9pY2VfY29tbWFuZDoKICAgIC0gSGV5IGVuZ2luZWVyICRtb2Rlczptb2RlCiAgICAtIEhleSBlbmdpbmVlciAkZW1vdGlvbnM6ZW1vdGlvbgogIHNsb3RzOgogICAgZW1vdGlvbnM6CiAgICAtIFNhZAogICAgLSBMb3ZlCiAgICAtIENvbmZ1c2VkCiAgICAtIFF1ZXN0aW9ucwogICAgLSBGdXJpb3VzCiAgICAtIEFuZ3J5CiAgICAtIENsb3NlIGV5ZXMKICAgIC0gVGlyZWQKICAgIC0gSGFwcHkKICAgIC0gRGVmYXVsdAogICAgbW9kZXM6CiAgICAtIEJ1ZmZldCBjb3Vyc2UKICAgIC0gTWFrZSBIdW5nYXJ5IGdyZWF0IGFnYWluCiAgICAtIERlZmF1bHQgbGlnaHRzCiAgbWFjcm9zOiB7fQoADwAAAAAAAAAGAAAAFAAAAB8AAAAoAAAANwAAAD8AAABIAAAAUAAAAFYAAABaAAAAXwAAAHgAAACCAAAAhgAAAIwAAABBbmdyeQBCdWZmZXQgY291cnNlAENsb3NlIGV5ZXMAQ29uZnVzZWQARGVmYXVsdCBsaWdodHMARGVmYXVsdABlbmdpbmVlcgBGdXJpb3VzAEhhcHB5AEhleQBMb3ZlAE1ha2UgSHVuZ2FyeSBncmVhdCBhZ2FpbgBRdWVzdGlvbnMAU2FkAFRpcmVkAAAAAAABAAAAAwAAAAUAAAAGAAAABwAAAAgAAAAJAAAACgAAAAsAAAAMAAAADQAAAA8AAAAQAAAAEQAAABIAAAAAAAAABQAAAA4AAAAWAAAAHAAAACIAAAAqAAAANAAAADoAAABBAAAASAAAAEwAAABOAAAAUQAAAGIAAABzAAAAewAAAH4AAACCAAAAAhgPHBIHAw4DHxQEHB0HAw4NFAQcHRQVGR0GJhQVGSYGJhQDFw4lIiYJCREOBBUfFQYfHQkRDgQVHwsXEwMXERwOJSEcEgMdEAIbEhANFQMjFg0UEAMYDwwSDxwNHwMPCxcWDRQQAxgPDBIPHA0fAw8NFxQkCx0IAxcmHQIJHwYMCQAABAAAAAAAAAAKAAAADQAAAA4AAAAPAAAAAAAAAAIAAAADAAAABQAAAAcAAAAIAAAACgAAAAwAAAANAAAADgAAAAEAAAAEAAAACwAAAAYAAAAJAAAAAAAAAAkAAAAPAAAAEAAAABEAAABlbW90aW9ucwBtb2RlcwAAAAAAAAAAAAAIAAAADQAAAA4AAAAPAAAAZW1vdGlvbgBtb2RlAAAAAAEAAAAAAAAADgAAAHZvaWNlX2NvbW1hbmQAAAABAAAAAAAAAP//////////AQAAABQAAAAAAAAAAwAAAP////8BAAAAKAAAABQAAAACAAAA/////wIAAABAAAAAUAAAACgAAAAAAAAAAAAAAAAAAAAoAAAAAQAAAAAAAAAAAAAAAAAAAA==",
  };
  const rhinoModel = { base64: modelParams };

  useEffect(() => {
    init(
      "+8P7CZmuTTw2Ock1VclK1XskRBAJlQiouUISmeCqaMWQAxWiJ+Rw3w==",
      rhinoContext,
      rhinoModel
    );
  }, []);

  useEffect(() => {
    if (inference !== null && inference.isFinalized) {
      console.log(inference?.slots["emotion"]);
      if (inference?.slots["emotion"]) {
        const emotions = [
          "Default",
          "Happy",
          "Tired",
          "Close eyes",
          "Angry",
          "Furious",
          "Sad",
          "Questions",
          "Confused",
          "Love",
        ];

        const emotion = emotions.indexOf(inference.slots["emotion"]);

        console.log(emotion);
        console.log(JSON.stringify({ id: `${emotion}` }));

        fetch("http://192.168.1.78:3000/emotion", {
          method: "POST",
          body: JSON.stringify({ id: `${emotion}` }),
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
          },
        });
      }
    }
  }, [inference]);

  useEffect(() => {
    if (!isListening) process();
  }, [inference, isListening, isLoaded]);

  return isLoaded && <h1>{isListening ? "Listening" : "Not listening"}</h1>;
}

export default VoiceWidget;

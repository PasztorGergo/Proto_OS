import { useCallback, useState } from "react";
import VoiceWidget from "./VoiceWidget";

function App() {
  const [hall, setHall] = useState(true);
  const [patriotism, setPatriotism] = useState(false);

  const setEmotion = useCallback((id) => {
    fetch("http://192.168.1.78:3000/emotion", {
      body: JSON.stringify({
        id,
      }),
      headers: {
        "Content-Type": "application/json",
      },
      method: "POST",
    });
  }, []);

  const toggleHall = useCallback(() => {
    setHall((prev) => !prev);
    fetch("http://192.168.1.78:3000/hall-effect", {
      body: JSON.stringify({
        state: !hall,
      }),
      headers: {
        "Content-Type": "application/json",
      },
      method: "POST",
    });
  }, [hall]);

  const togglePatriotism = useCallback(() => {
    setPatriotism((prev) => !prev);
    fetch("http://192.168.1.78:3000/hungary", {
      body: JSON.stringify({
        state: !patriotism,
      }),
      headers: {
        "Content-Type": "application/json",
      },
      method: "POST",
    });
  }, [patriotism]);

  return (
    <body className="relative [background-image:_radial-gradient(#26558C_0%,#090A20_65%)] min-h-screen pt-16">
      <header className="relative w-full py-4 lg:px-24 md:px-8 px-4 flex items-center justify-between">
        <div className="flex sm:flex-row flex-col gap-4 sm:gap-8 items-center h-full">
          <img
            width="64"
            height="64"
            alt="Scan logo"
            src="timer.svg"
            className="mix-blend-normal"
          />
          <h2 className="glow-text text-lg md:text-2xl lg:text-3xl uppercase">
            Bio scan
          </h2>
        </div>
        <div className="flex sm:flex-row flex-col items-center gap-4 sm:gap-8">
          <h2 className="uppercase sm:order-1 order-2 glow-text text-lg md:text-2xl lg:text-3xl">
            Threat level
          </h2>
          <div className="sm:order-2 order-1 min-w-fit flex flex-col items-center gap-4">
            <img className="h-12" src="range.svg" alt="Threat-o-meter" />
            <div className="bg-primary shadow-[0_0_8px_#9CEEFC] w-full h-[1px] relative flex items-center">
              <div
                className="absolute bg-primary shadow-[0_0_8px_#9CEEFC] w-4 h-4 [clip-path:polygon(50%_0%,_0%_100%,_100%_100%)]"
                id="triangle"
              />
            </div>
          </div>
        </div>
        <div className="absolute top-0 left-0 bg-primary-light w-full h-full mix-blend-soft-light" />
      </header>
      <main className="mt-16 lg:px-24 md:px-8 px-4 w-full grid md:grid-cols-3 grid-cols-1 md:gap-x-4 lg:gap-x-8 md:gap-y-0 gap-y-8">
        <nav className="">
          <h2 className="bg-primary-light bg-opacity-25 text-2xl glow-text w-full px-4 py-2 text-opacity-80 mb-8">
            Scan data
          </h2>
          <ul className="flex flex-col w-full text-white gap-2">
            <li className="md:pl-8 pl-4 pr-4 py-2 rounded-sm border bg-yellow-500 bg-opacity-80 border-primary-lighter border-opacity-25">
              <a href="/">Control panel</a>
            </li>
            <li className="md:pl-8 pl-4 pr-4 py-2 rounded-sm border border-primary-lighter border-opacity-25">
              <a href="/scans">HK-ReSe-024 type Protogen</a>
            </li>
            <li id="startButton">
              <VoiceWidget />
            </li>
          </ul>
        </nav>
        <section>
          <h2 className="bg-primary-light bg-opacity-25 text-2xl glow-text w-full px-4 py-2 text-opacity-80 mb-8">
            Emotions
          </h2>
          <ul className="max-h-80 glow-text flex md:flex-col md:flex-nowrap flex-wrap md:items-center gap-8 w-full overflow-y-scroll">
            <li
              className="emotion md:w-auto w-16"
              onClick={() => setEmotion(0)}
            >
              <img
                src="Default.png"
                title="Default"
                alt="Default"
                className="w-full h-full"
              />
            </li>
            <li
              className="emotion md:w-auto w-16"
              onClick={() => setEmotion(1)}
            >
              <img
                src="Happy.png"
                title="Happy"
                alt="Happy"
                className="w-full h-full"
              />
            </li>
            <li
              className="emotion md:w-auto w-16"
              onClick={() => setEmotion(2)}
            >
              <img
                src="Tired.png"
                title="Tired"
                alt="Tired"
                className="w-full h-full"
              />
            </li>
            <li
              className="emotion md:w-auto w-16"
              onClick={() => setEmotion(3)}
            >
              <img
                src="Eyes-closed.png"
                title="Eyes-closed"
                alt="Eyes-closed"
                className="w-full h-full"
              />
            </li>
            <li
              className="emotion md:w-auto w-16"
              onClick={() => setEmotion(4)}
            >
              <img
                src="Angry.png"
                title="Angry"
                alt="Angry"
                className="w-full h-full"
              />
            </li>
            <li
              className="emotion md:w-auto w-16"
              onClick={() => setEmotion(5)}
            >
              <img
                src="Furious.png"
                title="Furious"
                alt="Furious"
                className="w-full h-full"
              />
            </li>
            <li
              className="emotion md:w-auto w-16"
              onClick={() => setEmotion(6)}
            >
              <img
                src="Sad.png"
                title="Sad"
                alt="Sad"
                className="w-full h-full"
              />
            </li>
            <li
              className="emotion md:w-auto w-16"
              onClick={() => setEmotion(7)}
            >
              <img
                src="Inquestitive.png"
                title="Inquestitive"
                alt="Inquestitive"
                className="w-full h-full"
              />
            </li>
            <li
              className="emotion md:w-auto w-16"
              onClick={() => setEmotion(8)}
            >
              <img
                src="Confused.png"
                title="Confused"
                alt="Confused"
                className="w-full h-full"
              />
            </li>
            <li
              className="emotion md:w-auto w-16"
              onClick={() => setEmotion(9)}
            >
              <img
                src="Love.png"
                title="Love"
                alt="Love"
                className="w-full h-full"
              />
            </li>
          </ul>
        </section>
        <section className="flex flex-col gap-8">
          <h2 className="bg-primary-light bg-opacity-25 text-2xl glow-text w-full px-4 py-2 text-opacity-80">
            Functions
          </h2>
          <div>
            <h3 className="px-4 py-2 md:w-2/3 bg-[#74DC6E] bg-opacity-25 text-primary-light text-opacity-80">
              Primary
            </h3>
            <ul className="text-primary-light mt-4 flex flex-col gap-4">
              <li>Power</li>
              <li id="os"></li>
            </ul>
          </div>
          <div>
            <h3 className="px-4 py-2 md:w-2/3 bg-[#74DC6E] bg-opacity-25 text-primary-light text-opacity-80">
              Secondary
            </h3>
            <ul className="text-primary-light mt-4 flex flex-col gap-4">
              <li id="hall" className="flex items-center gap-4">
                <button
                  onClick={toggleHall}
                  className={`transition-all duration-500 rounded-full p-2 h-12 aspect-square ${
                    hall ? "on" : "off"
                  }`}
                  id="hall-btn"
                >
                  {hall ? "ON" : "OFF"}
                </button>
                Hall-effect sensor
              </li>
              <li className="flex items-center gap-4">
                <button
                  onClick={togglePatriotism}
                  className={`transition-all duration-500 rounded-full p-2 h-12 aspect-square ${
                    patriotism ? "huon" : "huoff"
                  }`}
                  id="hungary"
                >
                  {patriotism ? "ON" : "OFF"}
                </button>
                Patriotism mode
              </li>
              <li id="thermo">Thermomemter</li>
            </ul>
          </div>
        </section>
      </main>
    </body>
  );
}

export default App;

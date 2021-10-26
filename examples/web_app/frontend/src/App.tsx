import React from "react";
import "./App.css";
import * as types from './types'

// The player name and membership type we're searching for.
// The player name should include the code as well. i.e., Fate#1234
// The player type should be a string, i.e., Steam, Xbox, Stadia, PSN. etc.
// It could be null as well to return all memberships.
const PLAYER_NAME: types.str = "Fate怒#4275";
const PLAYER_TYPE: null | types.str = null;

function App(): JSX.Element {
  const [player, setPlayer] = React.useState<types.list<types.Player>>([]);

  const setPlayers = async (): Promise<void> => {
    await fetchPlayer().then((plr) => {
      // Set the JSON player payload.
      setPlayer(plr);
    });
  };

  // Make a POST request to our fast API.
  const fetchPlayer = async (): Promise<types.list<types.Player>> => {
    return await fetch("/player", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: PLAYER_NAME,
        type: PLAYER_TYPE,
      }),
    }).then((resp) => {
      return resp.json();
    });
  };

  React.useEffect(() => {
    setPlayers();
  }, []);

  return (
    <div className="App">
      {player?.map((plr) => {
        return (
          <h1 className="text">
            <img
              className="App-logo"
              src={`https://www.bungie.net${
                plr.iconPath !== null ? plr.iconPath : null
              }`}
            ></img>
            {plr.bungieGlobalDisplayName}#{plr.bungieGlobalDisplayNameCode}{" "}
            {plr.membershipId} | {plr.membershipType}
          </h1>
        );
      })}
    </div>
  );
}

export default App;

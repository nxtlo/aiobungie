import React from "react";
import "./App.css";

// Type aliases.
type int = number;
type str = string;
type bool = boolean;
type list<T extends Array<T>> = T[];

// An interface on what data the JSON player response will expect.
interface Player extends list<Player> {
  isPublic: bool;
  membershipType: int;
  membershipId: int;
  displayName: str;
  bungieGlobalDisplayName: str;
  bungieGlobalDisplayNameCode: int;
  iconPath: str;
}

// The player name and membership type we're searching for.
// The player name should include the code as well. i.e., Fate#1234
// The player type should be a string, i.e., Steam, Xbox, Stadia, PSN. etc.
// It could be null as well to return all memberships.
const PLAYER_NAME: string = "Fate怒#4275";
const PLAYER_TYPE: null | string = null;

function App(): JSX.Element {
  const [player, setPlayer] = React.useState<list<Player>>([]);

  const setPlayers = async (): Promise<void> => {
    await fetchPlayer().then((plr) => {
      // Set the JSON player payload.
      setPlayer(plr);
    });
  };

  // Make a POST request to our fast API.
  const fetchPlayer = async (): Promise<list<Player>> => {
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

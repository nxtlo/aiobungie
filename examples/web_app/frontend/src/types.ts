// Type aliases.
export type int = number;
export type str = string;
export type bool = boolean;
export type list<T extends Array<T>> = T[];

// An interface on what data the JSON player response will expect.
export interface Player extends list<Player> {
  isPublic: bool;
  membershipType: int;
  membershipId: int;
  displayName: str;
  bungieGlobalDisplayName: str;
  bungieGlobalDisplayNameCode: int;
  iconPath: str;
}

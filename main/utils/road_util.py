from typing import Set

from main.carcassonne_game_state import CarcassonneGameState
from main.objects.connection import Connection
from main.objects.coordinate import Coordinate
from main.objects.coordinate_with_side import CoordinateWithSide
from main.objects.meeple_position import MeeplePosition
from main.objects.road import Road
from main.objects.side import Side
from main.objects.terrain_type import TerrainType
from main.objects.tile import Tile


class RoadUtil:

    def opposite_edge(self, road_position: CoordinateWithSide):
        if road_position.side == Side.TOP:
            return CoordinateWithSide(Coordinate(road_position.coordinate.row - 1, road_position.coordinate.column),
                                      Side.BOTTOM)
        elif road_position.side == Side.RIGHT:
            return CoordinateWithSide(Coordinate(road_position.coordinate.row, road_position.coordinate.column + 1),
                                      Side.LEFT)
        elif road_position.side == Side.BOTTOM:
            return CoordinateWithSide(Coordinate(road_position.coordinate.row + 1, road_position.coordinate.column),
                                      Side.TOP)
        elif road_position.side == Side.LEFT:
            return CoordinateWithSide(Coordinate(road_position.coordinate.row, road_position.coordinate.column - 1),
                                      Side.RIGHT)

    def find_road(self, game_state: CarcassonneGameState, road_position: CoordinateWithSide) -> Road:
        roads: Set[CoordinateWithSide] = set(self.outgoing_roads_for_position(game_state, road_position))
        open_connections: Set[CoordinateWithSide] = set(map(lambda x: self.opposite_edge(x), roads))
        explored: Set[CoordinateWithSide] = roads.union(open_connections)
        while len(open_connections) > 0:
            open_connection: CoordinateWithSide = open_connections.pop()
            new_roads = self.outgoing_roads_for_position(game_state, open_connection)
            roads = roads.union(new_roads)
            new_open_connections = set(map(lambda x: self.opposite_edge(x), new_roads))
            explored = explored.union(new_roads)
            new_open_connection: CoordinateWithSide
            for new_open_connection in new_open_connections:
                if new_open_connection not in explored:
                    open_connections.add(new_open_connection)
                    explored.add(new_open_connection)

        finished: bool = len(explored) == len(roads)
        return Road(road_positions=roads, finished=finished)

    def outgoing_roads_for_position(self, game_state: CarcassonneGameState, road_position: CoordinateWithSide) -> [
        CoordinateWithSide]:
        tile: Tile = game_state.get_tile(road_position.coordinate.row, road_position.coordinate.column)
        if tile is None:
            return []

        roads: [CoordinateWithSide] = []

        connection: Connection
        for connection in tile.road:
            if connection.a == road_position.side or connection.b == road_position.side:
                if connection.a != Side.CENTER:
                    roads.append(CoordinateWithSide(coordinate=road_position.coordinate, side=connection.a))
                if connection.b != Side.CENTER:
                    roads.append(CoordinateWithSide(coordinate=road_position.coordinate, side=connection.b))

        return roads

    def road_contains_meeples(self, game_state: CarcassonneGameState, road: Road):
        for road_position in road.road_positions:
            for i in range(game_state.players):
                if road_position in list(map(lambda x: x.coordinate_with_side, game_state.placed_meeples[i])):
                    return True
        return False

    def find_meeples(self, game_state: CarcassonneGameState, road: Road) -> [[MeeplePosition]]:
        meeples: [[MeeplePosition]] = []

        for i in range(game_state.players):
            meeples.append([])

        for road_position in road.road_positions:
            for i in range(game_state.players):
                meeple_position: MeeplePosition
                for meeple_position in game_state.placed_meeples[i]:
                    if road_position == meeple_position.coordinate_with_side:
                        meeples[i].append(meeple_position)

        return meeples

    def find_roads(self, game_state: CarcassonneGameState, coordinate: Coordinate):
        roads: Set[Road] = set()

        tile: Tile = game_state.board[coordinate.row][coordinate.column]

        if tile is None:
            return roads

        side: Side
        for side in [Side.TOP, Side.RIGHT, Side.BOTTOM, Side.LEFT]:
            if tile.get_type(side) == TerrainType.ROAD:
                road: Road = self.find_road(game_state=game_state,
                                            road_position=CoordinateWithSide(coordinate=coordinate, side=side))
                roads.add(road)

        return list(roads)

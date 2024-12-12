from dataclasses import dataclass
import sys
from typing import List, Set, Dict
from common.utils import run, read_lines
from common.grid import BISHOP, ROOK, Cell, Point, grid_from_lines, Direction


@dataclass
class Region:
    name: str
    area: int
    perimeter: int
    points: Set[Point]


def solution_12_A(filename: str) -> int:
    lines = read_lines(filename)
    grid = grid_from_lines(lines)
    points_to_region: Dict[Point, Region] = dict()
    regions = list()
    valid_directions = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]

    for cell in grid:
        neighbour_vals = {d: cell.nav_val(d) for d in valid_directions}
        perimeter = len([v for v in neighbour_vals.values() if v is None or v != cell.val])

        if neighbour_vals[Direction.NORTH] == cell.val:
            region = points_to_region[cell.nav(Direction.NORTH).point]
            region.points.add(cell.point)
            region.area += 1
            region.perimeter += perimeter
            points_to_region[cell.point] = region

            # merge if attached to two different regions
            if neighbour_vals[Direction.WEST] == cell.val and region != points_to_region[cell.nav(Direction.WEST).point]:
                region_to_merge = points_to_region[cell.nav(Direction.WEST).point]
                points_to_region.update({p: region for p in region_to_merge.points})
                region.points |= region_to_merge.points
                region.area += region_to_merge.area
                region.perimeter += region_to_merge.perimeter
                regions.remove(region_to_merge)

        elif neighbour_vals[Direction.WEST] == cell.val:
            region = points_to_region[cell.nav(Direction.WEST).point]
            region.points.add(cell.point)
            region.area += 1
            region.perimeter += perimeter
            points_to_region[cell.point] = region
        
        else:
            region = Region(cell.val, 1, perimeter, {cell.point})
            points_to_region[cell.point] = region
            regions.append(region)

    total = 0
    for region in regions:
        total += (region.area * region.perimeter)
    return total

# corner when 
# o#    oo    #o
# ## or o# or o#
def is_corner(diag: bool, adj1: bool, adj2: bool) -> bool:
    return (adj1 == adj2 and not diag) or (diag and not adj1 and not adj2)


def corner_count(cell: Cell) -> int:
    same = {d: cell.val == cell.nav_val(d) for d in Direction}
    nw_corner = is_corner(same[Direction.NORTHWEST], same[Direction.NORTH], same[Direction.WEST])
    ne_corner = is_corner(same[Direction.NORTHEAST], same[Direction.NORTH], same[Direction.EAST])
    sw_corner = is_corner(same[Direction.SOUTHWEST], same[Direction.SOUTH], same[Direction.WEST])
    se_corner = is_corner(same[Direction.SOUTHEAST], same[Direction.SOUTH], same[Direction.EAST])
    return nw_corner + ne_corner + sw_corner + se_corner


def solution_12_B(filename: str) -> int:
    lines = read_lines(filename)
    grid = grid_from_lines(lines)
    points_to_region: Dict[Point, Region] = dict()
    regions: List[Region] = list()

    for cell in grid:
        neighbour_vals = {d: cell.nav_val(d) for d in ROOK}
        corners = corner_count(cell)

        if neighbour_vals[Direction.NORTH] == cell.val:
            region = points_to_region[cell.nav(Direction.NORTH).point]
            region.points.add(cell.point)
            region.area += 1
            region.perimeter += corners
            points_to_region[cell.point] = region

            # merge if attached to two different regions
            if neighbour_vals[Direction.WEST] == cell.val and region != points_to_region[cell.nav(Direction.WEST).point]:
                region_to_merge = points_to_region[cell.nav(Direction.WEST).point]
                points_to_region.update({p: region for p in region_to_merge.points})
                region.points |= region_to_merge.points
                region.area += region_to_merge.area
                region.perimeter += region_to_merge.perimeter
                regions.remove(region_to_merge)

        elif neighbour_vals[Direction.WEST] == cell.val:
            region = points_to_region[cell.nav(Direction.WEST).point]
            region.points.add(cell.point)
            region.area += 1
            region.perimeter += corners
            points_to_region[cell.point] = region
        
        else:
            region = Region(cell.val, 1, corners, {cell.point})
            points_to_region[cell.point] = region
            regions.append(region)

    total = 0
    for region in regions:
        total += (region.area * region.perimeter)
        print(f"{region.name}, {region.points.pop()}: {region.area} * {region.perimeter} = {region.area * region.perimeter}")
    return total


def test_solution_12_A():
    assert solution_12_A("./12/test_input1.txt") == 140
    assert solution_12_A("./12/test_input2.txt") == 772


# def test_final_solution_12_A():
#    assert solution_12_A('./12/input.txt') == 0 # Replace with solution when known


def test_solution_12_B():
    assert solution_12_B("./12/test_input1.txt") == 80
    assert solution_12_B("./12/test_input2.txt") == 436
    assert solution_12_B("./12/test_input3.txt") == 236
    assert solution_12_B("./12/test_input4.txt") == 1206


# def test_final_solution_12_B():
#    assert solution_12_B('./12/input.txt') == 0 # Replace with solution when known

if __name__ == "__main__":
    run("12", sys.argv[1], solution_12_A, solution_12_B)

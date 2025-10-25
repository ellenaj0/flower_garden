import random
from math import floor

from core.garden import Garden
from core.gardener import Gardener
from core.plants.plant_variety import PlantVariety
from core.plants.species import Species
from core.point import Position


class Gardener3(Gardener):
    def __init__(self, garden: Garden, varieties: list[PlantVariety]):
        super().__init__(garden, varieties)
        self.width = int(garden.width)
        self.height = int(garden.height)
        self.varieties = varieties
        self.species = [s.name for s in Species]

        self.species_varieties = self._init_species_varieties()
        self.variety_counts = {name: [v.name for v in varieties].count(name) for name in set(v.name for v in varieties)}
        print(f"width: {self.width}, height: {self.height}")
        print(self.species_varieties)
        print(self.variety_counts)

    def cultivate_garden(self) -> None:
        placements = self._get_hexagonal_placements()
        for variety, position in placements:
            res = self.garden.add_plant(variety, position)
            if res is None:
                print(f"failed to plant {variety} at pos {position}")

    
    def _get_hexagonal_placements(self) -> list:
        """Generate placements in a hexagonal grid pattern."""
        placements = []

        offsets = [0.0, 0.5]
        step_size = 1
        variety_indices = {s: 0 for s in self.species}
        for y in range(0, self.height + 1, step_size):
            offset = offsets[y % 2]
            for x in self._frange(offset, self.width + 0.1, step_size):
                position = Position(x, y)
                if y % 2 == 1:
                    species_name = self.species[(floor(x) + 2) % len(self.species)]
                else:
                    species_name = self.species[floor(x) % len(self.species)]

                variety = self.species_varieties[species_name][variety_indices[species_name]]
                variety_indices[species_name] += 1
                placements.append((variety, position))
                
        return placements

    # Taken from random_gardener.py
    def _get_random_placements(self) -> list:
        """Use random placements as fallback strategy."""
        random_placements = []
        for variety in self.varieties:
            x = random.uniform(0, self.garden.width)
            y = random.uniform(0, self.garden.height)

            position = Position(x, y)

            random_placements.append((variety, position))
        return random_placements
    
    def _init_species_varieties(self) -> dict:
        specs = {}
        for s in self.species:
            # unique_varieties = []
            # seen_names = set()
            # for variety in self.varieties:
            #     if variety.species.name == s and variety.name not in seen_names:
            #         unique_varieties.append(variety)
            #         seen_names.add(variety.name)
            specs[s] = [v for v in self.varieties if v.species.name == s]
        return specs
    

    def _frange(self, start: float, stop: float, step: float):
        while start < stop:
            yield start
            start += step


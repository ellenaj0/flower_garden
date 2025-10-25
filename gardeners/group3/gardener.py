import random
from collections import defaultdict

from core.garden import Garden
from core.gardener import Gardener
from core.plants.plant_variety import PlantVariety
from core.plants.species import Species
from core.point import Position

MIN_TOTAL_VARIETIES_COUNT = 10


class Gardener3(Gardener):
    def __init__(self, garden: Garden, varieties: list[PlantVariety]):
        super().__init__(garden, varieties)
        self.garden = garden
        self.width = int(garden.width)
        self.height = int(garden.height)
        self.varieties = varieties
        self.species = [s.name for s in Species]

        self.species_varieties = self._init_species_varieties()
        self.variety_counts = {name: [v.name for v in varieties].count(name) for name in set(v.name for v in varieties)}
        print(f"width: {self.width}, height: {self.height}")
        print(self.variety_counts)

    def cultivate_garden(self) -> None:
        try:
            placements = self._get_hexagonal_placements()
        except Exception as e:
            print(f"Hexagonal placement failed with error: {e}.\nFalling back to random placements.")
            placements = self._get_random_placements()

        for variety, position in placements:
            res = self.garden.add_plant(variety, position)
            if res is None:
                print(f"Failed to plant {variety} at pos {position}")


    def _get_hexagonal_placements(self) -> list:
        """Generate placements in a hexagonal grid pattern."""
        placements = []

        if len(self.varieties) < MIN_TOTAL_VARIETIES_COUNT:
            garden_width, garden_height = self.garden.width // 2, self.garden.height // 2
        else:
            garden_width, garden_height = self.garden.width, self.garden.height
        garden_internal = Garden(garden_width, garden_height)

        n_species = len(self.species)
        offsets = [0.0, 0.5]
        step_size = 1
        variety_indices = {s: 0 for s in self.species}

        # which species to try next for each row
        current_species_by_row = defaultdict(int)

        for y in range(0, self.height + 1, step_size):
            offset = offsets[y % 2]

            for x in self._frange(offset, self.width + 0.1, step_size):
                position = Position(x, y)

                current_species_idx = current_species_by_row[y]
                species_index = (current_species_idx + 2) % n_species if y % 2 == 1 else current_species_idx % n_species
                species_name = self.species[species_index]

                # skip if we've exhausted varieties for this species
                if variety_indices[species_name] >= len(self.species_varieties[species_name]):
                    # advance the index because there's nothing left for this species
                    current_species_by_row[y] = current_species_idx + 1
                    continue

                variety = self.species_varieties[species_name][variety_indices[species_name]]

                if garden_internal.can_place_plant(variety, position):
                    print(f"Placing {variety.name} at {position}")
                    placements.append((variety, position))
                    garden_internal.add_plant(variety, position)
                    variety_indices[species_name] += 1

                    # advance the index for this row only on successful placement
                    current_species_by_row[y] = current_species_idx + 1

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


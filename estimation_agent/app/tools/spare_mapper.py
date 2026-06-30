from rapidfuzz import process, fuzz


class SpareMapper:

    def __init__(self, available_spares):
        self.available_spares = available_spares

    def map_prediction(self, prediction):

        print("=" * 80)
        print("SPARE MAPPER START")
        print("=" * 80)

        mapped = []

        for spare in prediction.spares:

            print(f"\nGPT Returned: {spare.name}")

            match = process.extractOne(
                spare.name,
                self.available_spares,
                scorer=fuzz.WRatio
            )

            print("Match:", match)

            if match and match[1] >= 60:

                print("Mapped To:", match[0])

                spare.name = match[0]

                mapped.append(spare)

            else:

                print("No Match")

        prediction.spares = mapped

        return prediction
import pandas as pd
from amply import Amply

from otoole.read_strategies import ReadDatafile, ReadMemory


class TestReadMemoryStrategy:
    def test_read_memory(self):

        data = [
            ["SIMPLICITY", "ETH", 2014, 1.0],
            ["SIMPLICITY", "RAWSUG", 2014, 0.5],
            ["SIMPLICITY", "ETH", 2015, 1.03],
            ["SIMPLICITY", "RAWSUG", 2015, 0.51],
        ]
        df = pd.DataFrame(data=data, columns=["REGION", "FUEL", "YEAR", "VALUE"])
        parameters = {"AccumulatedAnnualDemand": df}

        actual, default_values = ReadMemory(parameters).read()

        expected = {
            "AccumulatedAnnualDemand": pd.DataFrame(
                data=data, columns=["REGION", "FUEL", "YEAR", "VALUE"]
            ).set_index(["REGION", "FUEL", "YEAR"])
        }

        assert "AccumulatedAnnualDemand" in actual.keys()
        pd.testing.assert_frame_equal(
            actual["AccumulatedAnnualDemand"], expected["AccumulatedAnnualDemand"]
        )


class TestConfig:
    def test_read_config(self):

        read = ReadDatafile()

        actual = read._read_config()
        expected = {
            "default": 0,
            "dtype": "float",
            "indices": ["REGION", "FUEL", "YEAR"],
            "type": "param",
        }
        assert actual["AccumulatedAnnualDemand"] == expected


class TestReadDatafile:
    def test_amply(self):

        Amply(
            """set REGION;
            # set REGION := SIMPLICITY;
            set TECHNOLOGY;
            set TECHNOLOGY := ETHPLANT GAS_EXTRACTION;
            set MODE_OF_OPERATION;
            set MODE_OF_OPERATION := 1 2;
            set YEAR;
            set YEAR := 2014;
            end;"""
        )

    def test_convert_amply_to_dataframe(self):

        config = {
            "VariableCost": {
                "type": "param",
                "indices": ["REGION", "TECHNOLOGY", "MODE_OF_OPERATION", "YEAR"],
                "dtype": "float",
                "default": 0,
            },
            "REGION": {"type": "set", "dtype": "str"},
            "YEAR": {"dtype": "int", "type": "set"},
            "MODE_OF_OPERATION": {"dtype": "int", "type": "set"},
            "TECHNOLOGY": {"dtype": "str", "type": "set"},
        }

        amply = Amply(
            """set REGION;
                        set REGION := SIMPLICITY;
                        set TECHNOLOGY;
                        set TECHNOLOGY := ETHPLANT GAS_EXTRACTION;
                        set MODE_OF_OPERATION;
                        set MODE_OF_OPERATION := 1 2;
                        set YEAR;
                        set YEAR := 2014;"""
        )
        amply.load_string(
            "param VariableCost {REGION,TECHNOLOGY,MODE_OF_OPERATION,YEAR};"
        )
        #     amply.load_string("""param default 0 : VariableCost :=
        # SIMPLICITY ETHPLANT 1 2014 2.89
        # SIMPLICITY ETHPLANT 2 2014 999999.0
        # SIMPLICITY GAS_EXTRACTION 1 2014 7.5
        # SIMPLICITY GAS_EXTRACTION 2 2014 999999.0""")
        amply.load_string(
            """
    param VariableCost default 0.0001 :=
    [SIMPLICITY,ETHPLANT,*,*]:
    2014 :=
    1 2.89
    2 999999.0
    [SIMPLICITY,GAS_EXTRACTION,*,*]:
    2014 :=
    1 7.5
    2 999999.0;"""
        )

        read = ReadDatafile()

        actual = read._convert_amply_to_dataframe(amply, config)
        expected = pd.DataFrame(
            data=[
                ["SIMPLICITY", "ETHPLANT", 1, 2014, 2.89],
                ["SIMPLICITY", "ETHPLANT", 2, 2014, 999999.0],
                ["SIMPLICITY", "GAS_EXTRACTION", 1, 2014, 7.5],
                ["SIMPLICITY", "GAS_EXTRACTION", 2, 2014, 999999.0],
            ],
            columns=["REGION", "TECHNOLOGY", "MODE_OF_OPERATION", "YEAR", "VALUE"],
        )
        print(actual, expected)
        pd.testing.assert_frame_equal(actual["VariableCost"], expected)

    def test_convert_amply_data_to_list_of_lists(self):

        data = {
            "SIMPLICITY": {
                "ETHPLANT": {1.0: {2014.0: 2.89}, 2.0: {2014.0: 999999.0}},
                "GAS_EXTRACTION": {1.0: {2014.0: 7.5}, 2.0: {2014.0: 999999.0}},
            }
        }
        expected = [
            ["SIMPLICITY", "ETHPLANT", 1.0, 2014.0, 2.89],
            ["SIMPLICITY", "ETHPLANT", 2.0, 2014.0, 999999.0],
            ["SIMPLICITY", "GAS_EXTRACTION", 1.0, 2014.0, 7.5],
            ["SIMPLICITY", "GAS_EXTRACTION", 2.0, 2014.0, 999999.0],
        ]
        read = ReadDatafile()
        actual = read._convert_amply_data_to_list(data)
        assert actual == expected

    def test_load_parameters(self):

        config = {"TestParameter": {"type": "param", "indices": ["index1", "index2"]}}
        read = ReadDatafile()
        actual = read._load_parameter_definitions(config)
        expected = "param TestParameter {index1,index2};\n"
        assert actual == expected

    def test_load_sets(self):

        config = {"TestSet": {"type": "set"}}

        read = ReadDatafile()
        actual = read._load_parameter_definitions(config)
        expected = "set TestSet;\n"
        assert actual == expected

    def test_catch_error_no_parameter(self, caplog):
        """Fix for https://github.com/OSeMOSYS/otoole/issues/70 where parameter in
        datafile but not in config causes error.  Instead, throw warning (and advise
        that user should use a custom configuration).
        """
        read = ReadDatafile()
        config = read.config
        amply_datafile = amply = Amply(
            """set REGION;
            set TECHNOLOGY;
            set MODE_OF_OPERATION;
            set YEAR;"""
        )
        amply.load_string("""param ResultsPath := 'test_path';""")
        read._convert_amply_to_dataframe(amply_datafile, config)
        assert (
            "Parameter ResultsPath could not be found in the configuration."
            in caplog.text
        )

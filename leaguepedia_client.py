from mwrogue.esports_client import EsportsClient


class LeaguepediaClient:

    def __init__(self, wiki='lol'):
        self.wiki = wiki
        self.site = EsportsClient(wiki)

    def get_current_regions(self):
        """
        Returns a list of current regions
        """
        try:

            response = self.site.cargo_client.query(
                tables="Regions=R",
                fields="R.RegionLong, R.IsCurrent",
                where="R.IsCurrent=1",
            )
        except:
            raise Exception("Error getting current regions")

        list_of_regions = [region['RegionLong'] for region in response]
        list_of_regions.append("International")
        # Since this is not a real region, we add it manually
        return list_of_regions

    def get_tournaments(self, region=None, date__gt=None, date__lt=None, year=None, name__contains=None):
        """
        Returns a list of tournaments
        :param region: Region of the tournament
        :param date__gt: Date greater than
        :param date__lt: Date less than
        :param year: Year of the tournament
        """
        response = None
        where_clauses = []

        if region is not None:
            where_clauses.append("T.Region='{}'".format(region))

        if date__gt is not None:
            where_clauses.append("T.Date>'{}'".format(date__gt))

        if date__lt is not None:
            where_clauses.append("T.Date<'{}'".format(date__lt))

        if year is not None:
            where_clauses.append("T.Date LIKE '%{}%'".format(year))

        if name__contains is not None:
            where_clauses.append("T.Name LIKE '%{}%'".format(name__contains))

        if where_clauses:
            where_clause = " AND ".join(where_clauses)
        else:
            where_clause = ""  # Empty WHERE clause to retrieve all data

        print(where_clause)
        response = self.site.cargo_client.query(
            tables="Tournaments=T",
            fields="T.Name, T.Region, T.Date",
            where=where_clause,
        )

        return response

    def manual_query(self, tables, join_on, fields, where):
        """
        Make a manual cargo query to the wiki
        :param tables: Tables to query
        :param fields: Fields to return
        :param where: Where clause
        """
        response = None

        response = self.site.cargo_client.query(
            tables=tables,
            join_on=join_on,
            fields=fields,
            where=where,
        )

        return response

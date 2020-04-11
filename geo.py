from phone_iso3166.country import phone_country
import flag

def get_country_name_and_flag(phone):
  try:
    country = phone_country(phone)
    return flag.flag(country) + country
  except:
    None
  return flag.flagize(":MX: MX")

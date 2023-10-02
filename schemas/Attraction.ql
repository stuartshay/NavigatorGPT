type Query {
  attraction(id: String!): Attraction
}

"""
Attraction
"""
type Attraction {
  """
  Id - Unique identifier for each attraction
  """
  id: String!

  """
  Title - Name of the attraction
  """
  title: String

  """
  FeatureKey - Feature Type
  """
  featureKey: String

  """
  Loc - Location
  """
  loc: Loc

  """
  Inventory - Inventory
  """
  inventory: Inventory

  """
  Aliases - List of Alternative Names Titles
  """
  aliases: [String!]

  """
  Photo - Main Photo
  """
  photo: Photo
}

"""
Location
"""
type Loc {
  """
  Latitude - WGS84
  """
  lat: Float

  """
  Longitude - WGS84
  """
  lon: Float

  """
  Location
  """
  location: String

  """
  SectorId
  """
  sectorId: String

  """
  Neighborhood
  """
  neighborhood: String

  """
  Address
  """
  address: String

  """
  Borough
  """
  borough: String

  """
  BoroughCode - Borough expressed as a two-character abbreviation (MN=Manhattan, BX=Bronx, BK=Brooklyn, QN=Queens, SI=Staten Island, N/A= Not Applicable ).
  """
  boroughCode: String

  """
  Block - The five-digit tax map block number, without leading zeros (ex. Block 00123 appears as 123).
  """
  block: Int

  """
  Lot - The four digit tax map lot number, without leading zeros (ex. Lot 0456 appears as 456).
  """
  lot: Int

  """
  BBL - Concatenation of the borough code (1=MN, 2=BX,3=BK,4=QN,5=SI), the five-digit tax map block, and the four-digit tax map lot numbers
  """
  bbl: Long

  """
  City
  """
  city: String

  """
  State
  """
  state: String

  """
  PostalCode - 5 Character US Zip Code
  Validation: ^\d{5}$
  """
  postalCode: String

  """
  Park - Park Name
  """
  park: String
  parkId: String
}

"""
Class representing a Photo.
"""
type Photo {
  """
  Photo Id
  """
  id: String!

  """
  Flickr PhotoId
  """
  photoId: Long!

  """
  Photo Title
  """
  title: String

  """
  Photo License
  """
  license: String!

  """
  Photo Author
  """
  author: String!

  """
  Photo Sizes
  """
  sizes: [PhotoSize!]!
}

"""
Attraction Inventory
"""
type Inventory {
  """
  Sculptors
  """
  sculptors: [String!]

  """
  Artist
  """
  artist: String

  """
  Architects
  """
  architects: [String!]

  """
  Carver
  """
  carver: String

  """
  Founder
  """
  founder: String

  """
  Dimensions
  """
  dimensions: String

  """
  Fabricator
  """
  fabricator: String

  """
  Materials
  """
  materials: String

  """
  Date
  """
  date: String

  """
  Cast Date
  """
  castDate: String

  """
  Dedicated
  """
  dedicated: String

  """
  Donor
  """
  donor: String

  """
  Provenance
  """
  provenance: String

  """
  Owner
  """
  owner: String

  """
  Styles
  """
  styles: [String!]
}

type PhotoSize {
  suffix: String

  """
  Label for the size
  """
  label: String

  """
  Width of the photo
  """
  width: Int!

  """
  Height of the photo
  """
  height: Int!

  """
  Url of the photo
  """
  url: String

  """
  Media type of the photo
  """
  mediaType: String
}

"""
The `Long` scalar type represents non-fractional signed whole 64-bit numeric values. Long can represent values between -(2^63) and 2^63 - 1.
"""
scalar Long

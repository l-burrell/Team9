
class Poster:

    clarity_rating = 0
    organization_rating = 0
    content_rating = 0
    relevance_rating = 0
    visual_appeal_rating = 0
    total_rating = 0

    def __init__(self, title: str, members: list, category: str, description: str):
        self.title = title
        self.members = members
        self.category = category
        self.description = description

    def calculateRating(self):
        overall_score = (self.clarity_rating + self.organization_rating + self.content_rating + self.relevance_rating + self.visual_appeal_rating)/100
        return overall_score
    
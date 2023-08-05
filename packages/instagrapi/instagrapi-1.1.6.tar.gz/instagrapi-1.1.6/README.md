# instagrapi

Fast and effective Instagram Private API wrapper (public+private requests and challenge resolver). Use the most recent version of the API from Instagram, which was obtained using [reverse-engineering with Charles Proxy](https://adw0rd.com/2020/03/26/sniffing-instagram-charles-proxy/en/).

Instagram API valid for 27 September 2020 (last reverse-engineering check)
Support Python>=3.6

### Features

1. Performs public (`_gql` or `_a1` suffix methods) or private/auth (`_v1` suffix methods) requests depending on the situation (to avoid Instagram limits)
2. Challenge Resolver have Email (as well as recipes for automating receive a code from email) and SMS handlers
3. Support upload a Photo, Video, IGTV, Albums and Stories
4. Support work with User, Media, Insights, Collections and Direct objects
5. Insights by posts and stories
6. Build stories with custom background and font animation

### Install

    pip install instagrapi

### Tests

    python -m unittest tests
    python -m unittest tests.ClientPublicTestCase

### Requests

* `Public` (anonymous) methods had suffix `_gql` (Instagram `GraphQL`) or `_a1` (example `https://www.instagram.com/adw0rd/?__a=1`)
* `Private` (authorized request) methods have `_v1` suffix

The first request to fetch media/user is `public` (anonymous), if instagram raise exception, then use `private` (authorized).
Example (pseudo-code):

```
def media_info(media_pk):
    try:
        return self.media_info_gql(media_pk)
    except ClientError as e:
        # Restricted Video: This video is not available in your country.
        # Or media from private account
        return self.media_info_v1(media_pk)
```

### Usage

```
from instagrapi import Client

cl = Client()
cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)

user_id = cl.user_id_from_username("adw0rd")
medias = cl.user_medias(user_id, 20)
```

#### Account

This is your authorized account

| Method                                                   | Return   | Description                                                   |
| -------------------------------------------------------- | -------- | ------------------------------------------------------------- |
| login(username: str, password: str, settings: dict = {}) | Bool     | Login by username and password                                |
| relogin()                                                | Bool     | Relogin with clean cookies (required cl.username/cl.password) |
| login_by_sessionid(sessionid: str)                       | Bool     | Login by sessionid from Instagram site                        |
| get_settings()                                           | Dict     | Return settings dict (more details below)                     |
| set_proxy(dsn: str)                                      | Dict     | Support socks and http/https proxy                            |
| cookie_dict                                              | Dict     | Return cookies                                                |
| user_id                                                  | Int      | Return you user_id (after login)                              |
| device                                                   | Dict     | Return device dict which we pass to Instagram                 |
| set_device(device: dict)                                 | None     | Change device settings                                        |
| set_user_agent(user_agent: str)                          | None     | Change User-Agent header                                      |
| base_headers                                             | Dict     | Base headers for Instagram                                    |

Example:

```
cl.login("instagrapi", "42")
# cl.login_by_sessionid("peiWooShooghahdi2Eip7phohph0eeng")
cl.set_proxy("socks5://127.0.0.1:30235")
# cl.set_proxy("http://127.0.0.1:8080")

print(cl.get_settings())
print(cl.user_info(cl.user_id))
```

You can pass settings to the Client (and save cookies), it has the following format:

```
settings = {
   "uuids": {
      "phone_id": "57d64c41-a916-3fa5-bd7a-3796c1dab122",
      "uuid": "8aa373c6-f316-44d7-b49e-d74563f4a8f3",
      "client_session_id": "6c296d0a-3534-4dce-b5aa-a6a6ab017443",
      "advertising_id": "8dc88b76-dfbc-44dc-abbc-31a6f1d54b04",
      "device_id": "android-e021b636049dc0e9"
   },
   "cookies":  {},  # set here you saved cookies
   "last_login": 1596069420.0000145,
   "device_settings": {
      "cpu": "h1",
      "dpi": "640dpi",
      "model": "h1",
      "device": "RS988",
      "resolution": "1440x2392",
      "app_version": "117.0.0.28.123",
      "manufacturer": "LGE/lge",
      "version_code": "168361634",
      "android_release": "6.0.1",
      "android_version": 23
   },
   "user_agent": "Instagram 117.0.0.28.123 Android (23/6.0.1; ...US; 168361634)"
}

cl = Client(username, password, settings=settings)
```

This values send to Instagram API.

#### Media

Viewing and editing publications (medias)

* `media_id` - String ID `"{media_id}_{user_id}"`, example `"2277033926878261772_1903424587"` (Instagram terminology)
* `media_pk` - Integer ID (real media id), example `2277033926878261772` (Instagram terminology)
* `code` - Short code (slug for media), example `BjNLpA1AhXM` from `"https://www.instagram.com/p/BjNLpA1AhXM/"`
* `url` - URL to media publication

| Method                                             | Return             | Description                                                   |
| -------------------------------------------------- | ------------------ | ------------------------------------------------------------- |
| media_id(media_pk: int)                            | Str                | Return media_id by media_pk                                   |
| media_pk(media_id: str)                            | Int                | Return media_pk by media_id                                   |
| media_pk_from_code(code: str)                      | Int                | Return media_pk                                               |
| media_pk_from_url(url: str)                        | Int                | Return media_pk                                               | 
| media_info(media_pk: int)                          | Dict\[full media]  | Return media info                                             |
| media_delete(media_pk: int)                        | Bool               | Delete media                                                  |
| media_edit(media_pk: int, caption: str)            | Bool               | Change caption for media                                      |
| media_user(media_pk: int)                          | Dict\[user]        | Get user info for media                                       |
| media_oembed(url: str)                             | Dict\[short media] | Return short media info by media URL                          | 
| media_comment(media_id: str, message: str)         | Bool               | Write message to media                                        | 
| media_comments(media_id: str)                      | List\[comment]     | Get all comments                                              |

Example:

```
>>> cl.media_pk_from_code("B-fKL9qpeab")
2278584739065882267

>>> cl.media_pk_from_code("B8jnuB2HAbyc0q001y3F9CHRSoqEljK_dgkJjo0")
2243811726252050162

>>> cl.media_pk_from_url("https://www.instagram.com/p/BjNLpA1AhXM/")
1787135824035452364

>>> cl.media_oembed("https://www.instagram.com/p/B3mr1-OlWMG/")
{'version': '1.0',
 'title': 'В гостях у ДК @delai_krasivo_kaifui',
 'author_name': 'adw0rd',
 'author_url': 'https://www.instagram.com/adw0rd',
 'author_id': 1903424587,
 'media_id': '2154602296692269830_1903424587',
 'provider_name': 'Instagram',
 'provider_url': 'https://www.instagram.com',
 'type': 'rich',
 'width': 658,
 'height': None,
 'html': '<blockquote>...',
 'thumbnail_url': 'https://instagram.frix7-1.fna.fbcdn.net/v....135355164531920_1445273950655800983_n.jpg',
 'thumbnail_width': 640,
 'thumbnail_height': 480,
 'can_view': True}

```

#### User

View a list of a user's medias, following and followers

* `user_id` - Integer ID of user, example `1903424587`

| Method                                             | Return       | Description                                                   |
| -------------------------------------------------- | ------------ | ------------------------------------------------------------- |
| user_medias(user_id: int, amount: int = 20)        | List\[media] | Get list of medias by user_id                                 |
| user_followers(user_id: int)                       | Dict         | Get dict {user_id: user, ...} of followers users              |
| user_following(user_id: int)                       | Dict         | Get dict {user_id: user, ...} of following users              |
| user_info(user_id: int)                            | Dict\[user]  | Get user info                                                 |
| user_info_by_username(username: str)               | Dict\[user]  | Get user info by username                                     |
| user_follow(user_id: int)                          | Bool         | Follow user                                                   |
| user_unfollow(user_id: int)                        | Bool         | Unfollow user                                                 |
| user_id_from_username(username: str)               | Int          | Get user_id by username                                       |
| username_from_user_id(user_id: int)                | Str          | Get username by user_id                                       |

Example:

```
>>> cl.user_followers(cl.user_id).keys()
dict_keys([5563084402, 43848984510, 1498977320, ...])

>>> cl.user_following(cl.user_id)
{
   8530598273: {
      "pk": 8530598273,
      "username": "dhbastards",
      "full_name": "The Best DH Skaters Ever",
      "is_private": False,
      "profile_pic_url": "https://instagram.frix7-1.fna.fbcdn.net/v/t5...9318717440_n.jpg",
      "is_verified": False
  },
  ...
}

>>> cl.user_info_by_username('adw0rd')
{'pk': 1903424587,
 'username': 'adw0rd',
 'full_name': 'Mikhail Andreev',
 'is_private': False,
 'profile_pic_url': 'https://scontent-arn2-1.cdninstagram.com/v/t51...FB463C5',
 'is_verified': False,
 'media_count': 102,
 'follower_count': 578,
 'following_count': 529,
 'biography': 'Engineer: Python, JavaScript, Erlang\n@dhbastards ...',
 'external_url': 'https://adw0rd.com/',
 'is_business': False}
 
```

#### Upload Media as Post (to Feed)

| Method                                             | Return       | Description                                                                     |
| -------------------------------------------------- | ------------ | ------------------------------------------------------------------------------- |
| photo_upload(path, caption)                        | Dict\[media] | Upload photo (Support JPG files)                                                |
| photo_download(media_pk)                           | Str\[path]   | Download photo (Return path to photo with best resoluton)                       |
| video_upload(path, caption)                        | Dict\[media] | Upload video (Support mp4 files)                                                |
| video_download(media_pk)                           | Str\[path]   | Download video (Return path to video with best resoluton)                       |
| igtv_upload(path, title, caption)                  | Dict\[media] | Upload IGTV (Support mp4 files)                                                 |
| igtv_download(media_pk)                            | Str\[path]   | Download IGTV (Return path to video with best resoluton)                        |
| album_upload(paths, caption)                       | Dict\[media] | Upload Album (Support JPG and mp4)                                              |
| album_download(media_pk)                           | List\[path]   | Download Album (Return multiple paths to photo and video with best resolutons) |

#### Stories

Upload medias to you stories. Common arguments:

* `filepath` - Path to media file
* `caption` - Caption for story (now use to fetch mentions)
* `thumbnail` - Thumbnail instead capture from source file
* `usertags` - Specify usertags for mention users in story 
* `configure_timeout` - How long to wait in seconds for a response from Instagram when publishing a story
* `links` - "Swipe Up" links (now use first)

| Method                                                                                                                                       | Return       | Description                      |
| -------------------------------------------------------------------------------------------------------------------------------------------- | ------------ | -------------------------------- |
| photo_upload_to_story(filepath: str, caption: str, thumbnail: str = None, usertags: list = [], configure_timeout: int = 3, links: list = []) | Dict\[media] | Upload photo (Support JPG files) |
| video_upload_to_story(filepath: str, caption: str, thumbnail: str = None, usertags: list = [], configure_timeout: int = 3, links: list = []) | Dict\[media] | Upload video (Support mp4 files).  |

Examples:

```
path = cl.video_download(
    cl.media_pk_from_url('https://www.instagram.com/p/CGgDsi7JQdS/')
)
cl.video_upload_to_story(
    path,
    "Credits @adw0rd",
    usertags=[
        {'user': {'pk': 1903424587, 'name': 'adw0rd'}, 'x': 0.49892962, 'y': 0.703125, 'width': 0.8333333333333334, 'height': 0.125}
    ],
    links=[{'webUri': 'https://adw0rd.com/'}]
)
```

#### Collections

| Method                                                       | Return             | Description                                                   |
| ------------------------------------------------------------ | ------------------ | ------------------------------------------------------------- |
| collections()                                                | List\[collection]  | Get all account collections                                   |
| collection_medias_by_name(name)                              | List\[media]       | Get medias in collection by name                              |
| collection_medias(collection_id, amount=21, last_media_pk=0) | List\[media]       | Get medias in collection by collection_id; Use **amount=0** to return all medias in collection; Use **last_media_pk** to return medias by delta |

#### Insights

In the process of describing

#### Direct

In the process of describing

#### Challenge

In the process of describing

### Common Exceptions

| Exception                 | Base        | Description                          |
| ------------------------- | ----------- |------------------------------------- |
| ClientError               | Exception   | Base Exception for Instagram calls   |
| GenericRequestError       | ClientError | Base Exception for Request           |
| ClientGraphqlError        | ClientError | Exception for GraphQL calls          |
| ClientJSONDecodeError     | ClientError | JSON Exception                       |
| ClientConnectionError     | ClientError | Connection error                     |
| ClientBadRequestError     | ClientError | HTTP 400 Exception                   |
| ClientForbiddenError      | ClientError | HTTP 403 Exception                   |
| ClientNotFoundError       | ClientError | HTTP 404 Exception                   |
| ClientThrottledError      | ClientError | HTTP 429 Exception                   |
| ClientRequestTimeout      | ClientError | Request Timeout Exception            |
| ClientIncompleteReadError | ClientError | Raised when response interrupted     |
| ClientLoginRequired       | ClientError | Raised when Instagram required Login |
| ReloginAttemptExceeded    | ClientError | Raised when all attempts exceeded    |

### Private Exceptions

| Exception                | Base         | Description                                                 |
| ------------------------ | ------------ |------------------------------------------------------------ |
| PrivateError             | ClientError  | Base Exception for Private calls (received from Instagram)  |
| FeedbackRequired         | PrivateError | Raise when get message=feedback_required                    |
| LoginRequired            | PrivateError | Raise when get message=login_required                       |
| SentryBlock              | PrivateError | Raise when get message=sentry_block                         |
| RateLimitError           | PrivateError | Raise when get message=rate_limit_error                     |
| BadPassword              | PrivateError | Raise when get message=bad_password                         |
| UnknownError             | PrivateError | Raise when get unknown message (new message from instagram) |

### Challenge Exceptions

| Exception                      | Base           | Description                                                 |
| ------------------------------ | -------------- |------------------------------------------------------------ |
| ChallengeError                 | PrivateError   | Base Challenge Exception (received from Instagram)          |
| ChallengeRedirection           | ChallengeError | Raise when get type=CHALLENGE_REDIRECTION                   |
| ChallengeRequired              | ChallengeError | Raise when get message=challenge_required                   |
| SelectContactPointRecoveryForm | ChallengeError | Raise when get challengeType=SelectContactPointRecoveryForm |
| RecaptchaChallengeForm         | ChallengeError | Raise when get challengeType=RecaptchaChallengeForm         |
| SubmitPhoneNumberForm          | ChallengeError | Raise when get challengeType=SubmitPhoneNumberForm          |

### Media Exceptions

| Exception                | Base         | Description                                    |
| ------------------------ | ------------ |----------------------------------------------- |
| MediaError               | PrivateError | Base Media Exception (received from Instagram) |
| MediaNotFound            | MediaError   | Raise when user unavailable                    |

### User Exceptions

| Exception                | Base          | Description                                   |
| ------------------------ | ------------- |---------------------------------------------- |
| UserError                | PrivateError  | Base User Exception (received from Instagram) |
| UserNotFound             | UserError     | Raise when user unavailable                   |

### Collection Exceptions

| Exception                | Base            | Description                                         |
| ------------------------ | --------------- |---------------------------------------------------- |
| CollectionError          | PrivateError    | Base Collection Exception (received from Instagram) |
| CollectionNotFound       | CollectionError | Raise when collection unavailable                   |

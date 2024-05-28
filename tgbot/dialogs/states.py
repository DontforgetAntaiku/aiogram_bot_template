from aiogram.fsm.state import State, StatesGroup


class NewUser(StatesGroup):
    channel_name = State()
    more = State()
    ton_wallet = State()
    trust_wallet = State()


class NewNote(StatesGroup):
    project_name = State()
    project_link = State()
    channel_name = State()
    status = State()


class NewCoordinatedAd(StatesGroup):
    project_name = State()
    project_link = State()
    project_rep = State()
    channel_name = State()
    channel_rep = State()
    date_to_post = State()
    time_to_place = State()
    wallet_type = State()
    price = State()
    # ton_address = State()
    note = State()


class AcceptingStage(StatesGroup):
    link_button = State()
    confirm = State()


class AdminStatistic(StatesGroup):
    start = State()

    all_notes = State()
    i_note = State()

    all_coordinated_uncompleted_ads = State()
    i_coordinated_uncompleted_ad = State()

    all_available_channels = State()
    show_available_channels = State()

    all_data_to_excel = State()

    get_channel_name = State()
    all_uncompleted_channel_ads = State()
    i_channel_post = State()

    what_to_export = State()


class UserStatistics(StatesGroup):
    start = State()

    all_uncompleted_channel_rep_ads = State()
    i_uncompleted_channel_rep_ads = State()

    all_channel_rep_ads = State()
    i_channel_rep_ads = State()

=====
Usage
=====

Using person in a project::

    from personroles import person

Using Name::

    name = person.Name("Hans Hermann", "Bayer")
    print(name)

    Name:
    first_name=Hans
    last_name=Bayer
    middle_name_1=Hermann

Using Noble::

    noble = person.Noble("Dagmara", "Bodelschwingh", peer_title="Gräfin von")
    print(noble)

    Noble:
    first_name=Dagmara
    last_name=Bodelschwingh
    peer_preposition=von
    peer_title=Gräfin

Using Academic::

    academic = person.Academic("Horst Heiner", "Wiekeiner",
                               academic_title="Dr.")
    print(academic)

    Academic:
    academic_title=Dr.
    first_name=Horst
    last_name=Wiekeiner
    middle_name_1=Heiner

Using Person::

    person_1 = person.Person("Sven", "Rübennase", academic_title="MBA", born="1990")
    print(person_1)

    Person:
    academic_title=MBA
    age=30
    born=1990
    first_name=Sven
    gender=male
    last_name=Rübennase

Using Politician::

    from personroles import politician_role

    politician = politician_role.Politician("SPD", "Bärbel", "Gutherz", academic_title="Dr.",
                                   date_of_birth="1980")
    print(politician)

    Politician:
    academic_title=Dr.
    age=40
    born=1980
    first_name=Bärbel
    gender=female
    last_name=Gutherz
    parties=[Party(party_name='SPD', party_entry='unknown', party_exit='unknown')]
    party_name=SPD

    politician.add_Party("GRÜNE", party_entry="2017")

    print(politician)

    Politician:
    ...
    parties=[Party(party_name='SPD', party_entry='unknown', party_exit='unknown'),
             Party('GRÜNE', party_entry='2017', party_exit='unknown')]
    party_name='GRÜNE'

Using MoP::

    from personroles import mop_role

    mop = mop_role.MoP("14", "Grüne", "Tom", "Schwadronius", peer_title="Junker von",
                     born="1950")
    print(mop)

    MoP:
    age=70
    born=1950
    first_name=Tom
    gender=male
    last_name=Schwadronius
    legislature=14
    membership={14}
    parties=[Party(party_name='Grüne', party_entry='unknown', party_exit='unknown')]
    party=Grüne
    peer_preposition=von
    peer_title=Junker

    mop.add_Party("Grüne")
    mop.change_ward("Düsseldorf II")
    print(mop)

    MoP:
    age=70
    born=1950
    electoral_ward=Düsseldorf II
    first_name=Tom
    gender=male
    last_name=Schwadronius
    legislature=14
    membership={14}
    parties=[Party(party_name='SPD', party_entry='unknown', party_exit='unknown'),
             Party('GRÜNE', party_entry='unknown', party_exit='unknown')]
    party_name=Grüne
    peer_preposition=von
    peer_title=Junker
    voter_count=99022
    ward_no=41

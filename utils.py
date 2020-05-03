def labels_diff(changes):
    previous_labels = set([item["title"] for item in changes["previous"]])
    current_labels = set([item["title"] for item in changes["current"]])

    return {
        "label_added": current_labels - previous_labels,
        "label_removed": previous_labels - current_labels,
    }


def labels_sync(source, destination, sync_filter):
    for l in destination.copy():
        if sync_filter(l):
            if l not in source:
                destination.remove(l)

    for l in source.copy():
        if sync_filter(l):
            if l not in destination:
                destination.add(l)

    return destination

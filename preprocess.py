from datasets import load_dataset
import os

dataset = load_dataset('xnli', "all_languages")
train_data_per_lang = {}
validation_data_per_lang = {}
test_data_per_lang = {}

lang_map = {}

for part in ["train", "validation", "test"]:
    print(part)
    for i in range(len(dataset[part])):
        data_obj = dataset[part][i]
        
        premise_obj = data_obj["premise"]
        hypothesis_lang_list = data_obj["hypothesis"]["language"]
        translation_list = data_obj["hypothesis"]["translation"]
        label = data_obj["label"]
        
        for j in range(len(hypothesis_lang_list)):
            lang = hypothesis_lang_list[j]
            lang_map[lang] = True
            hypothesis = translation_list[j]
            premise = premise_obj[lang]
            
            assert len(hypothesis) == len(hypothesis.replace("\t",""))
            assert len(premise) == len(premise.replace("\t",""))

            if part == "train":
                if lang not in train_data_per_lang:
                    train_data_per_lang[lang] = []
                train_data_per_lang[lang].append([i, premise, hypothesis, label])
            elif part == "validation":
                if lang not in validation_data_per_lang:
                    validation_data_per_lang[lang] = []
                validation_data_per_lang[lang].append([i, premise, hypothesis, label])
            else:
                if lang not in test_data_per_lang:
                    test_data_per_lang[lang] = []
                test_data_per_lang[lang].append([i, premise, hypothesis, label])

for lang in lang_map:
    print(f"train {lang} :", len(train_data_per_lang[lang]))
    print(f"validation {lang} :", len(validation_data_per_lang[lang]))
    print(f"test {lang} :", len(test_data_per_lang[lang]))
    with open(f"xnli_train_{lang}.tsv", "w+") as f:
        f.write("id\tpremise\thypothesis\tlabel\n")
        for obj in train_data_per_lang[lang]:
            f.write(str(obj[0]) + "\t" + obj[1] + "\t" + obj[2] + "\t" + str(obj[3]) + "\n")
    with open(f"xnli_validation_{lang}.tsv", "w+") as f:
        f.write("id\tpremise\thypothesis\tlabel\n")
        for obj in validation_data_per_lang[lang]:
            f.write(str(obj[0]) + "\t" + obj[1] + "\t" + obj[2] + "\t" + str(obj[3]) + "\n")
    with open(f"xnli_test_{lang}.tsv", "w+") as f:
        f.write("id\tpremise\thypothesis\tlabel\n")
        for obj in test_data_per_lang[lang]:
            f.write(str(obj[0]) + "\t" + obj[1] + "\t" + obj[2] + "\t" + str(obj[3]) + "\n")   

    os.system(f"zip -r xnli_train_{lang}.zip xnli_train_{lang}.tsv")
    os.system(f"zip -r xnli_validation_{lang}.zip xnli_validation_{lang}.tsv")
    os.system(f"zip -r xnli_test_{lang}.zip xnli_test_{lang}.tsv")
    os.system(f"rm xnli_train_{lang}.tsv")
    os.system(f"rm xnli_validation_{lang}.tsv")
    os.system(f"rm xnli_test_{lang}.tsv")